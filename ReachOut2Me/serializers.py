from rest_framework import serializers, viewsets
from .models import Post, Comment, Message, FriendRequest,  UserProfile

class PostSerializer(serializers.ModelSerializer):
    
    class Meta:
        fields = '__all__'
        model = Post

class CommentSerializer(serializers.ModelSerializer):
    
    class Meta:
        fields = '__all__'
        model = Comment

class MessageSerializer(serializers.ModelSerializer):
    
    class Meta:
        fields = '__all__'
        model = Message

class FriendRequestSerializer(serializers.ModelSerializer):
    
    class Meta:
        fields = '__all__'
        model = FriendRequest

class UserProfileSerializer(serializers.ModelSerializer):
    class Meta:
        model = UserProfile
        fields = '__all__'

class UserProfileViewSet(viewsets.ModelViewSet):
    queryset = UserProfile.objects.all()
    serializer_class = UserProfileSerializer