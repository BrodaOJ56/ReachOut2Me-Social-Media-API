from rest_framework import serializers, viewsets
from .models import Post, Comment, Message, UserProfile, User, CommentReply, Notification, CommentReplyLike, Follow
from dj_rest_auth.registration.serializers import RegisterSerializer
from dj_rest_auth.registration.views import RegisterView
from django.dispatch import receiver
from django.db.models.signals import post_save
from django.conf import settings
from drf_spectacular.utils import extend_schema_field


class PostSerializer(serializers.ModelSerializer):
    # set the author field to a required field
    author = serializers.CharField(required=False)

    # define the fields that will be serialized/deserialized
    class Meta:
        # set the fields to all fields in the Post model
        fields = '__all__'
        # set the model to the Post model
        model = Post


class CommentSerializer(serializers.ModelSerializer):
    # set the author field to a string representation of the author
    author = serializers.StringRelatedField()
    # set the required for the image fields to False
    # the use_url=True means that the image will be returned as a URL
    image = serializers.ImageField(required=False, use_url=True)

    class Meta:
        fields = '__all__'
        model = Comment

    # override the create method to allow the creation of a comment with an image
    def create(self, validated_data):
        # get the request from the context
        request = self.context.get('request')
        # get the image from the request
        image = request.FILES.get('image')
        validated_data.pop('image', None)  # remove the 'image' key from validated_data
        # create the comment
        comment = Comment.objects.create(
            author=request.user,
            # set the image to the image from the request if it exists and None otherwise
            image=image if image else None,
            **validated_data
        )
        return comment


class CommentSerializer(serializers.ModelSerializer):
    likes = serializers.SerializerMethodField()

    @extend_schema_field(str)
    def get_likes(self, obj):
        return str(obj.likes.count())

    class Meta:
        model = Comment
        fields = ['id', 'author', 'post', 'likes']

class CommentReplySerializer(serializers.ModelSerializer):
    class Meta:
        fields = '__all__'
        model = CommentReply


class MessageSerializer(serializers.ModelSerializer):
    class Meta:
        fields = '__all__'
        model = Message


class UserProfileSerializer(serializers.ModelSerializer):
    class Meta:
        model = UserProfile
        fields = '__all__'


class UserProfileViewSet(viewsets.ModelViewSet):
    queryset = UserProfile.objects.all()
    serializer_class = UserProfileSerializer


class UploadAvatarSerializer(serializers.ModelSerializer):
    class Meta:
        model = UserProfile
        fields = ('avatar',)


class UserSerializer(serializers.ModelSerializer):
    class Meta:
        model = User
        fields = ['id', 'username', 'email', 'first_name', 'last_name']


class UserProfile_Serializer(serializers.ModelSerializer):
    # getting this fields from the UserSerializer
    username = serializers.CharField(source='user.username')
    email = serializers.EmailField(source='user.email')
    first_name = serializers.CharField(source='user.first_name')
    last_name = serializers.CharField(source='user.last_name')
    date_joined = serializers.DateTimeField(source='user.date_joined')

    class Meta:
        model = UserProfile
        fields = '__all__'


class NotificationSerializer(serializers.ModelSerializer):
    class Meta:
        model = Notification
        fields = '__all__'


class NameRegistrationSerializer(RegisterSerializer):
    first_name = serializers.CharField(required=False)
    last_name = serializers.CharField(required=False)

    def custom_signup(self, request, user):
        user.first_name = self.validated_data.get('first_name', '')
        user.last_name = self.validated_data.get('last_name', '')
        user.save(update_fields=['first_name', 'last_name'])


@receiver(post_save, sender=settings.AUTH_USER_MODEL)
def create_user_profile(sender, instance, created, **kwargs):
    if created:
        UserProfile.objects.create(user=instance)


class NameRegistrationView(RegisterView):
    serializer_class = NameRegistrationSerializer


class CommentReplyLikeSerializer(serializers.ModelSerializer):
    user = serializers.ReadOnlyField(source='user.username')
    comment_reply = serializers.PrimaryKeyRelatedField(queryset=CommentReply.objects.all())

    class Meta:
        model = CommentReplyLike
        fields = ['id', 'user', 'comment_reply']
        read_only_fields = ['id']


class FollowUserSerializer(serializers.Serializer):
    user_id = serializers.IntegerField()

    def validate_user_id(self, value):
        try:
            user = User.objects.get(id=value)
        except User.DoesNotExist:
            raise serializers.ValidationError("User with id={} does not exist".format(value))
        return user

    def create(self, validated_data):
        user_to_follow = validated_data['user_id']
        current_user = self.context['request'].user
        current_user_profile, created = UserProfile.objects.get_or_create(user=current_user)
        if user_to_follow == current_user:
            raise serializers.ValidationError("You can't follow yourself")
        if user_to_follow in current_user_profile.following.all():
            raise serializers.ValidationError("You are already following this user")
        current_user_profile.following.add(user_to_follow)
        current_user_profile.save()
        return {'success': 'User followed successfully'}
    
class ResponseSerializer(serializers.Serializer):
    success = serializers.BooleanField(default=False)
    error = serializers.CharField(allow_blank=True, default='')

    def create(self, validated_data):
        return validated_data

    def update(self, instance, validated_data):
        instance.update(validated_data)
        return instance
    
class FollowerSerializer(serializers.ModelSerializer):
    id = serializers.ReadOnlyField(source='follower.id')
    username = serializers.ReadOnlyField(source='follower.username')

    class Meta:
        model = Follow
        fields = ['id', 'username']

class UserSerializer(serializers.ModelSerializer):
    class Meta:
        model = User
        fields = ['id', 'username']