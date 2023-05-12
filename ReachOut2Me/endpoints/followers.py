from rest_framework.decorators import api_view
from rest_framework.response import Response
from rest_framework import status
from django.contrib.contenttypes.models import ContentType

from ..models import UserProfile, User, Follow, Notification
from ..serializers import FollowUserSerializer, ResponseSerializer, FollowerSerializer, UserSerializer
from drf_spectacular.utils import extend_schema


# Decorator indicates that this function can handle HTTP POST requests
@extend_schema(
    tags=['followers'],
    request=None, # Add this line to specify the serializer used for the request data
    responses={ # Add this line to specify the response schema
        status.HTTP_200_OK: ResponseSerializer,
        status.HTTP_400_BAD_REQUEST: ResponseSerializer,
        status.HTTP_404_NOT_FOUND: ResponseSerializer,
    }
)
@api_view(['POST'])
# Takes the request object and the ID of the user to follow as parameters
def follow_user(request, user_id):
    try:
        # Try to retrieve the user to follow by ID
        user_to_follow = User.objects.get(id=user_id)
    except User.DoesNotExist:
        # If the user is not found, return a 404 error response
        return Response({"error": "User not found"}, status=status.HTTP_404_NOT_FOUND)

    # Retrieve the current user from the request object
    current_user = request.user
    # Check if the current user is the same as the user to follow
    if current_user == user_to_follow:
        return Response({"error": "You can't follow yourself"}, status=status.HTTP_400_BAD_REQUEST)

    try:
        # Try to retrieve the user profile for the current user
        current_user_profile = UserProfile.objects.get(user=current_user)
    except UserProfile.DoesNotExist:
        # If the profile does not exist, create a new one
        current_user_profile = UserProfile.objects.create(user=current_user)

    # Check if the user to follow is already in the current user's following list
    if user_to_follow in current_user_profile.following.all():
        return Response({"error": "You are already following this user"}, status=status.HTTP_400_BAD_REQUEST)

    # Create an instance of the FollowUserSerializer with the input data
    serializer = FollowUserSerializer(data={'user_id': user_id})

    # Validate the serializer input
    if not serializer.is_valid():
        return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)

    # Add the user to follow to the current user's following list
    current_user_profile.following.add(user_to_follow)
    # Save the user profile
    current_user_profile.save()
    # Create the notification object
    notification = Notification(
        recipient=user_to_follow,  # User who will receive the notification
        actor_object_id=current_user.id,  # ID of the user who performed the action (following)
        actor_content_type=ContentType.objects.get_for_model(current_user),  # Content type of the actor object (user)
        verb='started following you',  # Notification message
        actor_object=current_user,  # Actor object (user who performed the action)
    )
    notification.save()
    # Return a success response
    return Response({"success": "User followed successfully"}, status=status.HTTP_200_OK)



@extend_schema(
    tags=['followers'],
    request=None,
    responses={200: ResponseSerializer}
)
@api_view(['POST'])
def unfollow_user(request, user_id):
    try:
        # Try to retrieve the user to unfollow by ID
        user_to_unfollow = User.objects.get(id=user_id)
    except User.DoesNotExist:
        # If the user is not found, return a 404 error response
        return Response({"error": "User not found"}, status=status.HTTP_404_NOT_FOUND)

    # Retrieve the current user from the request object
    current_user = request.user

    # Check if the current user is the same as the user to unfollow
    if current_user == user_to_unfollow:
        # If so, return a 400 error response
        return Response({"error": "You can't unfollow yourself"}, status=status.HTTP_400_BAD_REQUEST)

    # Retrieve the user profile for the current user
    current_user_profile, created = UserProfile.objects.get_or_create(user=current_user)

    # Check if the user to unfollow is in the current user's following list
    if user_to_unfollow not in current_user_profile.following.all():
        # If not, return a 400 error response
        return Response({"error": "You are not following this user"}, status=status.HTTP_400_BAD_REQUEST)

    # Remove the user to unfollow from the current user's following list
    current_user_profile.following.remove(user_to_unfollow)
    # Save the user profile
    current_user_profile.save()

    # Return a success response
    return Response({"success": "User unfollowed successfully"}, status=status.HTTP_200_OK)


@extend_schema(
    tags=['followers'],
    request=FollowUserSerializer,
        responses={200: ResponseSerializer},
)
@api_view(['GET'])
def followers_list(request, user_id):
    try:
        # Try to retrieve the user by ID
        user = User.objects.get(id=user_id)
    except User.DoesNotExist:
        # If the user is not found, return a 404 error response
        return Response({"error": "User not found"}, status=status.HTTP_404_NOT_FOUND)

    # Retrieve all followers for the user
    followers = Follow.objects.filter(following=user)

    # Serialize the followers data
    serializer = FollowerSerializer(followers, many=True)

    # Return the serialized data as a JSON response
    return Response(serializer.data, status=status.HTTP_200_OK)

@extend_schema(
    tags=['followers'],
    request=None,
    responses={200: UserSerializer}

)
@api_view(['GET'])
def following_list(request, user_id):
    try:
        # Try to retrieve the user by ID
        user = User.objects.get(id=user_id)
    except User.DoesNotExist:
        # If the user is not found, return a 404 error response
        return Response({"error": "User not found"}, status=status.HTTP_404_NOT_FOUND)

    # Retrieve all the users that the given user is following
    following = UserProfile.objects.filter(following=user).values_list('user', flat=True)
    # Retrieve the user objects for the users that the given user is following
    following_users = User.objects.filter(id__in=following)

    # Serialize the list of following users
    serializer = UserSerializer(following_users, many=True)

    # Return the serialized list of following users as a JSON response
    return Response(serializer.data, status=status.HTTP_200_OK)

