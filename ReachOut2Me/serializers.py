from rest_framework import serializers, viewsets
from .models import Post, Comment, Message, FriendRequest, UserProfile, User


class PostSerializer(serializers.ModelSerializer):
    class Meta:
        fields = '__all__'
        model = Post


class CommentSerializer(serializers.ModelSerializer):
    author = serializers.StringRelatedField()
    image = serializers.ImageField(required=False, use_url=True)

    class Meta:
        fields = '__all__'
        model = Comment

    def create(self, validated_data):
        request = self.context.get('request')
        image = request.FILES.get('image')
        validated_data.pop('image', None)  # remove the 'image' key from validated_data
        comment = Comment.objects.create(
            author=request.user,
            image=image,
            **validated_data
        )
        return comment


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


class UploadAvatarSerializer(serializers.ModelSerializer):
    class Meta:
        model = UserProfile
        fields = ('avatar',)


class UserSerializer(serializers.ModelSerializer):
    class Meta:
        model = User
        fields = ['id', 'username', 'email', 'first_name', 'last_name']


class UserProfile_Serializer(serializers.ModelSerializer):
    username = serializers.CharField(source='user.username')
    email = serializers.EmailField(source='user.email')
    first_name = serializers.CharField(source='user.first_name')
    last_name = serializers.CharField(source='user.last_name')
    date_joined = serializers.DateTimeField(source='user.date_joined')

    class Meta:
        model = UserProfile
        fields = ['id', 'username', 'email',
                  'first_name', 'last_name', 'date_of_birth',
                  'avatar', 'bio', 'date_joined', 'gender',
                  'country', 'state_or_city', 'telephone_number'
                  ]
