from ..models import User, UserProfile
from rest_framework.views import APIView
from rest_framework.response import Response
from rest_framework.authentication import TokenAuthentication
from rest_framework.permissions import IsAuthenticated, AllowAny
from rest_framework import status
from ..serializers import UserProfileSerializer, \
    UploadAvatarSerializer, UserProfile_Serializer


# Just testing out the APIView for the get all users endpoint
class GetAllUsers(APIView):
    # authentication_classes = [TokenAuthentication]
    permission_classes = [AllowAny]

    def get(self, request):
        users = UserProfile.objects.all()
        serializer = UserProfile_Serializer(users, many=True)
        return Response(serializer.data, status=status.HTTP_200_OK)


class GetUserProfile(APIView):
    def get(self, request):
        users = UserProfile.objects.filter(user=request.user).first()
        serializer = UserProfile_Serializer(users)
        return Response(serializer.data, status=status.HTTP_200_OK)


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
    def put(self, request):
        user_profile = request.user
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


# search by username
class SearchUserView(APIView):
    def get(self, username):
        # query the database and get the user by username
        user = User.objects.filter(username=username).first()
        # if user is not found, return a 404 error
        if not user:
            return Response(
                {'error': 'User with that username not found.',
                 'message': 'Please check the username and try again.'
                 },
                status=status.HTTP_404_NOT_FOUND)
        # serializer
        serializer = UserProfile_Serializer(user)
        # if user is found, return the user
        return Response(serializer.data, status=status.HTTP_200_OK)
