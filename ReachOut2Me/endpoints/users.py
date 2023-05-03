from ..models import User, UserProfile
from rest_framework.views import APIView
from rest_framework.response import Response
from rest_framework.authentication import TokenAuthentication
from rest_framework.permissions import IsAuthenticated, AllowAny
from rest_framework import status
from ..serializers import UserProfileSerializer, \
    UploadAvatarSerializer, UserProfile_Serializer, UserSerializer
from ..utils import validate_country


# view to get all users
class GetAllUsers(APIView):
    # Allow any user (authenticated or not) to hit this endpoint.
    permission_classes = [AllowAny]

    # get method to get all users
    def get(self, request):
        # query the UserProfile table in the database to get all users
        users = UserProfile.objects.all()
        # serialize the data passing in the users object as the data
        # many=True because we are serializing a list of objects
        serializer = UserProfile_Serializer(users, many=True)
        # return the serialized data with a status code of 200
        return Response(serializer.data, status=status.HTTP_200_OK)


# view to get a single user
class GetUserProfile(APIView):
    # this can only be accessed by authenticated users
    # get method to get a single user
    def get(self, request):
        # query the UserProfile table in the database to get a single user using the logged-in user
        users = UserProfile.objects.filter(user=request.user).first()
        # if user is found, serialize the data and return it with a status code of 200
        serializer = UserProfile_Serializer(users)
        return Response(serializer.data, status=status.HTTP_200_OK)


# view to get and update a user profile
class UserProfileView(APIView):
    def get(self, request):
        # query the UserProfile table in the database to get a single user using the logged-in user
        user_profile = UserProfile.objects.filter(user=request.user).first()
        # if user is found, serialize the data and return it with a status code of 200
        if user_profile:
            serializer = UserProfileSerializer(user_profile)
            return Response(serializer.data, status=status.HTTP_200_OK)
        # if user is not found, return an error message with a status code of 404
        else:
            return Response({'error': 'User profile not found.'}, status=status.HTTP_404_NOT_FOUND)

    # put method to update a user profile
    def put(self, request):
        # query the UserProfile table in the database to get a single user using the logged-in user
        user_profile = UserProfile.objects.filter(user=request.user).first()
        # if user is not found, return an error message with a status code of 404
        if not user_profile:
            return Response({'error': 'User profile not found.'}, status=status.HTTP_404_NOT_FOUND)
        # if the user tries to update his/her profile
        if request.data:
            # create a dictionary to store the data
            data = {}
            # loop through the data sent by the user
            for key, value in request.data.items():
                # if the key is date_of_birth, store the value in the dictionary without stripping it or converting it to lowercase
                if key == 'date_of_birth':
                    data[key] = value
                # if the key is not date_of_birth, store the value in the dictionary after stripping it and converting it to lowercase
                else:
                    data[key] = value.strip().lower()
            # if the user tries to update his/her telephone number
            if 'telephone_number' in data:
                # check if the telephone number is not empty and if it is not a number
                # if it is empty and also not a number, return an error message with a status code of 400
                if data['telephone_number'] and not data['telephone_number'].isdigit():
                    return Response({'error': 'Telephone number must be a number.'}, status=status.HTTP_400_BAD_REQUEST)
            # we can comment this block of code if we want to host since we will be using select tag for the country field

            # if the user tries to update his/her country
            if 'country' in data:
                # if the country input sent is not empty
                if data['country']:
                    # validate the country to see if the country is an existing country
                    # the validate_country function is defined in the utils.py file
                    country = validate_country(data['country'])
                    # if the country is not valid, then return an error message with a status code of 400
                    if not country:
                        return Response({'error': 'Invalid country'}, status=status.HTTP_400_BAD_REQUEST)
            # end of block of code to comment
            # serialize the data
            # the partial=True allows partial update, you don't need to provide all fields for update
            serializer = UserProfileSerializer(user_profile, data=data, partial=True)
        # if the user is not sending a data, do nothing. This will prevent the program from throwing errors
        else:
            serializer = UserProfileSerializer(user_profile, data=request.data, partial=True)
        # if the serializer is valid, save the data and return it with a status code of 200
        if serializer.is_valid():
            serializer.save()
            return Response(serializer.data)
        # if the serializer is not valid, return the error message with a status code of 400
        else:
            return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)


# view to upload a user avatar
class UploadAvatarView(APIView):
    # this can only be accessed by authenticated users
    # put method to upload a user avatar
    def put(self, request):
        # set the user_profile to the logged-in user
        user_profile = request.user
        # if user is not found, return an error message with a status code of 404
        if not user_profile:
            return Response({'error': 'User profile not found.'}, status=status.HTTP_404_NOT_FOUND)

        # query the database to get the user avatar
        user_avatar = UserProfile.objects.filter(user=user_profile).first()
        # serialize the data passing in the user_avatar object as the data to be serialized and the request.data
        serializer = UploadAvatarSerializer(user_avatar, data=request.data)
        # if the serializer is valid, save the data and return a success message with a status code of 200
        if serializer.is_valid():
            serializer.save()
            return Response({'success': 'Avatar uploaded successfully.'}, status=status.HTTP_200_OK)
        # if the serializer is not valid, return the error message with a status code of 400
        else:
            return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)


# view to get a single user by username
class SearchUserView(APIView):
    def get(self, request, username):
        # query the database and get the user by username
        user = User.objects.filter(username=username).first()
        # if user is not found, return a 404 error
        if not user:
            return Response(
                {'error': 'User with that username not found.',
                 'message': 'Please check the username and try again.'
                 },
                status=status.HTTP_404_NOT_FOUND)
        # if the user is found, query the UserProfile table in the database to get the user profile
        exact_user = UserProfile.objects.filter(user=user).first()
        # serializer
        serializer = UserProfile_Serializer(exact_user)
        # return the serialized data with a status code of 200
        return Response(serializer.data, status=status.HTTP_200_OK)
