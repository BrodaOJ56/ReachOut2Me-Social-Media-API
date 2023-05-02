from rest_framework.decorators import api_view
from rest_framework.response import Response
from rest_framework import status

from ..models import UserProfile, User, Follow
from ..serializers import UserProfile_Serializer


# Decorator indicates that this function can handle HTTP POST requests
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
    # Add the user to follow to the current user's following list
    current_user_profile.following.add(user_to_follow)
    # Save the user profile
    current_user_profile.save()
    # Return a success response
    return Response({"success": "User followed successfully"}, status=status.HTTP_200_OK)



@api_view(['POST'])
def unfollow_user(request, user_id):
    try:
        user_to_unfollow = User.objects.get(id=user_id)
    except User.DoesNotExist:
        return Response({"error": "User not found"}, status=status.HTTP_404_NOT_FOUND)
    
    current_user = request.user
    if current_user == user_to_unfollow:
        return Response({"error": "You can't unfollow yourself"}, status=status.HTTP_400_BAD_REQUEST)
    
    current_user_profile = UserProfile.objects.get(user=current_user)
    
    if user_to_unfollow not in current_user_profile.following.all():
        return Response({"error": "You are not following this user"}, status=status.HTTP_400_BAD_REQUEST)
    
    current_user_profile.following.remove(user_to_unfollow)
    current_user_profile.save()
    
    return Response({"success": "User unfollowed successfully"}, status=status.HTTP_200_OK)


@api_view(['GET'])
def followers_list(request, user_id):
    try:
        user = User.objects.get(id=user_id)
    except User.DoesNotExist:
        return Response({"error": "User not found"}, status=status.HTTP_404_NOT_FOUND)

    followers = Follow.objects.filter(following=user)
    followers_list = [{'id': follower.follower.id, 'username': follower.follower.username} for follower in followers]
    
    return Response(followers_list, status=status.HTTP_200_OK)
