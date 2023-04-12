from ..models import User, UserProfile
from rest_framework.views import APIView
from rest_framework.response import Response
from rest_framework import status
from ..serializers import UserProfileSerializer


# Just testing out the APIView for the get all users endpoint
class GetAllUsers(APIView):
    def get(self, request):
        users = User.objects.select_related('userprofile').all()
        all_users = []
        for user in users:
            if user.email:
                user.email = user.email
            else:
                user.email = 'No email provided'
            all_users.append({
                'username': user.username,
                'email': user.email,
                'is_staff': user.is_staff,
                'is_active': user.is_active,
                'is_superuser': user.is_superuser,
                'date_joined': user.date_joined,
                'last_login': user.last_login,
                'bio': user.userprofile.bio if hasattr(user, 'userprofile') else 'No bio available',
            })
        return Response(all_users, status=status.HTTP_200_OK)
    
    
#Endpoint to register as a new user
class RegisterUser(APIView):
    def post(self, request):
        data = request.data
        required_fields = ['username', 'password', 'first_name', 'last_name', 'email']
        if not all(field in data for field in required_fields):
            return Response({'error': 'Username, password, first name, last name, and email are required.'},
                            status=status.HTTP_400_BAD_REQUEST)
        
        #convert input to lowercase before saving to the database
        data['username'] = data['username'].lower()
        data['email'] = data['email'].lower()
        user = User.objects.create_user(**data)
        return Response({'success': f'User {user.username} registered.'}, status=status.HTTP_201_CREATED)


class UserProfileView(APIView):
    def get(self, request):
        user_profile = UserProfile.objects.filter(user=request.user).first()
        if user_profile:
            serializer = UserProfileSerializer(user_profile)
            return Response(serializer.data)
        else:
            return Response({'error': 'User profile not found.'}, status=status.HTTP_404_NOT_FOUND)

    def put(self, request):
        user_profile = UserProfile.objects.filter(user=request.user).first()
        if not user_profile:
            return Response({'error': 'User profile not found.'}, status=status.HTTP_404_NOT_FOUND)

        serializer = UserProfileSerializer(user_profile, data=request.data)
        if serializer.is_valid():
            serializer.save()
            return Response(serializer.data)
        else:
            return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)