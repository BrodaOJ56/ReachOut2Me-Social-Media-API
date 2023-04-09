from rest_framework import serializers
from .models import Post, Comment, Message, FriendRequest

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