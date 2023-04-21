from rest_framework.views import APIView
from rest_framework.response import Response
from rest_framework import status
from ..models import User, UserProfile
from ..utils import validate_email, validate_password
from rest_framework.authtoken.models import Token
from rest_framework.authtoken.views import ObtainAuthToken
from rest_framework.permissions import AllowAny


# Endpoint to register as a new user
class RegisterUser(APIView):
    permission_classes = [AllowAny]

    def post(self, request):
        data = request.data
        required_fields = ['username', 'password', 'first_name', 'last_name', 'email']
        if not all(field in data for field in required_fields):
            return Response({'error': 'Username, password, first name, last name, and email are required.'},
                            status=status.HTTP_400_BAD_REQUEST)
        username_exist = User.objects.filter(username=data['username'].lower()).exists()
        email_exist = User.objects.filter(email=data['email'].lower()).exists()
        if username_exist:
            return Response({'error': 'Username already exists.'}, status=status.HTTP_400_BAD_REQUEST)
        if email_exist:
            return Response({'error': 'Email already exists.'}, status=status.HTTP_400_BAD_REQUEST)
        if not validate_email(data['email'].lower()):
            return Response({'error': 'Email is invalid.'}, status=status.HTTP_400_BAD_REQUEST)
        if not validate_password(data['password']):
            return Response({'error 1': 'Password must be at least 8 characters long.',
                            'error 2': 'Password must contain at least one uppercase letter.',
                             'error 3': 'Password must contain at least one lowercase letter.',
                             'error 4': 'Password must contain at least one number.',
                             'error 5': 'Password must not contain spaces.'
                             }, status=status.HTTP_400_BAD_REQUEST)
        # convert input to lowercase before saving to the database
        data['username'] = data['username'].lower()
        data['email'] = data['email'].lower()
        data['first_name'] = data['first_name'].lower()
        data['last_name'] = data['last_name'].lower()
        user = User.objects.create_user(**data)
        UserProfile.objects.create(user=user)
        return Response({'success': f'User {user.username} registered.'}, status=status.HTTP_201_CREATED)


class LoginView(ObtainAuthToken):
    def post(self, request, *args, **kwargs):
        # convert the username to lowercase
        request.data['username'] = request.data['username'].lower()
        serializer = self.serializer_class(data=request.data,
                                           context={'request': request})
        serializer.is_valid(raise_exception=True)
        user = serializer.validated_data['user']
        token, created = Token.objects.get_or_create(user=user)
        return Response({
            'token': token.key,
            'user_id': user.pk,
            'email': user.email
        })


class LogoutView(APIView):
    def post(self, request):
        request.user.auth_token.delete()
        return Response(
            {"message": "Successfully logged out."},
            status=status.HTTP_200_OK)
