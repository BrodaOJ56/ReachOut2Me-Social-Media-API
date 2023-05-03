from rest_framework.views import APIView
from rest_framework.response import Response
from rest_framework import status
from ..models import User, UserProfile
from ..utils import validate_email, validate_password
from rest_framework.authtoken.models import Token
from rest_framework.authtoken.views import ObtainAuthToken
from rest_framework.permissions import AllowAny


# View to register as a new user
class RegisterUser(APIView):
    # Allow any user (authenticated or not) to hit this endpoint.
    permission_classes = [AllowAny]

    # post method to register a new user
    def post(self, request):
        # get the data from the request
        data = request.data
        # list of required fields
        required_fields = ['username', 'password', 'first_name', 'last_name', 'email']
        # check if all required fields are present
        # if not, return an error
        if not all(field in data for field in required_fields):
            return Response({'error': 'Username, password, first name, last name, and email are required.'},
                            status=status.HTTP_400_BAD_REQUEST)
        # check if username already exists
        username_exist = User.objects.filter(username=data['username'].lower()).exists()
        # check if email already exists
        email_exist = User.objects.filter(email=data['email'].lower()).exists()
        # if username or email already exists, return an error message with a status code of 400
        if username_exist:
            return Response({'error': 'Username already exists.'}, status=status.HTTP_400_BAD_REQUEST)
        # if email already exists, return an error message with a status code of 400
        if email_exist:
            return Response({'error': 'Email already exists.'}, status=status.HTTP_400_BAD_REQUEST)
        # check if email is valid
        # the validate_email function is defined in utils.py
        # if email is not valid, return an error message with a status code of 400
        if not validate_email(data['email'].lower()):
            return Response({'error': 'Email is invalid.'}, status=status.HTTP_400_BAD_REQUEST)
        # check if password is valid
        # the validate_password function is defined in utils.py
        # if password is not valid, return the error messages stating the requirements for a valid password with a status code of 400
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
        # create a new user and pass the data
        user = User.objects.create_user(**data)
        # create a new user profile using the user object
        UserProfile.objects.create(user=user)
        # return a success message with a status code of 201 after a successful registration
        return Response({'success': f'User {user.username} registered.'}, status=status.HTTP_201_CREATED)


# view to log in a user
class LoginView(ObtainAuthToken):
    # the ObtainAuthToken class is from rest_framework.authtoken.views
    # it is used to generate a token for a user after a successful login
    # the token is used to authenticate the user for subsequent requests
    def post(self, request, *args, **kwargs):
        # convert the username to lowercase
        request.data['username'] = request.data['username'].lower()
        # pass the request to the ObtainAuthToken class
        serializer = self.serializer_class(data=request.data,
                                           context={'request': request})
        # raise an exception if the serializer is not valid
        serializer.is_valid(raise_exception=True)
        # get the user object from the serializer
        user = serializer.validated_data['user']
        # get the token for the user if it exists, if not, create a new token
        token, created = Token.objects.get_or_create(user=user)
        # return the token, user id, and email
        return Response({
            'token': token.key,
            'user_id': user.pk,
            'email': user.email
        })


# view to log out a user
class LogoutView(APIView):
    # post method to log out a user
    def post(self, request):
        # check if the user is authenticated
        # the request.user object is created by the TokenAuthentication class
        # if the user is not authenticated, return an error message with a status code of 401
        # if the user is authenticated, delete the token and return a success message with a status code of 200
        request.user.auth_token.delete()
        return Response(
            {"message": "Successfully logged out."},
            status=status.HTTP_200_OK)
