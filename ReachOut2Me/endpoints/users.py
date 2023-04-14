from ..models import User, UserProfile
from rest_framework.views import APIView
from rest_framework.response import Response
from rest_framework import status
from ..serializers import UserProfileSerializer, UploadAvatarSerializer, UserProfile_Serializer
from ..utils import validate_email


# Just testing out the APIView for the get all users endpoint
class GetAllUsers(APIView):
    def get(self, request):
        # users = User.objects.select_related('userprofile').all()
        users = UserProfile.objects.all()
        serializer = UserProfile_Serializer(users, many=True)
        return Response(serializer.data, status=status.HTTP_200_OK)
        # all_users = []
        # for user in users:
        #     if user.email:
        #         user.email = user.email
        #     else:
        #         user.email = 'No email provided'
        #     if hasattr(user, 'userprofile') and user.userprofile.avatar:
        #         avatar = user.userprofile.avatar.url
        #     else:
        #         avatar = 'No avatar available'
        #     if hasattr(user, 'userprofile') and user.userprofile.bio:
        #         bio = user.userprofile.bio
        #     else:
        #         bio = 'No bio available'
        #     all_users.append({
        #         'id': user.id,
        #         'username': user.username,
        #         'email': user.email,
        #         'is_superuser': user.is_superuser,
        #         'date_joined': user.date_joined,
        #         'avatar': avatar,
        #         'bio': bio
        #     })
        # return Response(all_users, status=status.HTTP_200_OK)


# Endpoint to register as a new user
class RegisterUser(APIView):
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
        # convert input to lowercase before saving to the database
        data['username'] = data['username'].lower()
        data['email'] = data['email'].lower()
        data['first_name'] = data['first_name'].lower()
        data['last_name'] = data['last_name'].lower()
        user = User.objects.create_user(**data)
        UserProfile.objects.create(user=user)
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


# we will implement the current user when we implement authentication/login
class UploadAvatarView(APIView):
    def put(self, request, pk):
        # user_profile = UserProfile.objects.filter(user=request.user).first()
        # user_profile = User.objects.get(id=pk)
        user_profile = User.objects.filter(id=pk).first()   # This works fine to display the error message
        if not user_profile:
            return Response({'error': 'User profile not found.'}, status=status.HTTP_404_NOT_FOUND)

        user_avatar = UserProfile.objects.filter(user=user_profile).first()
        # if not user_avatar:
        #     UserProfile.objects.create(user=user_profile)
        #     user_avatar = UserProfile.objects.filter(user=user_profile).first()

        serializer = UploadAvatarSerializer(user_avatar, data=request.data)
        if serializer.is_valid():
            serializer.save()
            return Response({'success': 'Avatar uploaded successfully.'}, status=status.HTTP_200_OK)
        else:
            return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)
