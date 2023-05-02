from rest_framework.decorators import api_view
from rest_framework.response import Response
from rest_framework import status

from ..models import UserProfile, User, Follow
from ..serializers import UserProfile_Serializer

@api_view(['POST'])
def follow_user(request, user_id):
    try:
        user_to_follow = User.objects.get(id=user_id)
    except User.DoesNotExist:
        return Response({"error": "User not found"}, status=status.HTTP_404_NOT_FOUND)
    
    current_user = request.user
    if current_user == user_to_follow:
        return Response({"error": "You can't follow yourself"}, status=status.HTTP_400_BAD_REQUEST)
    
    try:
        current_user_profile = UserProfile.objects.get(user=current_user)
    except UserProfile.DoesNotExist:
        current_user_profile = UserProfile.objects.create(user=current_user)
    
    if user_to_follow in current_user_profile.following.all():
        return Response({"error": "You are already following this user"}, status=status.HTTP_400_BAD_REQUEST)
    
    current_user_profile.following.add(user_to_follow)
    current_user_profile.save()
    
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
