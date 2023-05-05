from rest_framework import serializers, viewsets
from .models import Post, Comment, Message, UserProfile, User, CommentReply, Notification
from dj_rest_auth.registration.serializers import RegisterSerializer
from dj_rest_auth.registration.views import RegisterView


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


class NameRegistrationView(RegisterView):
    serializer_class = NameRegistrationSerializer
