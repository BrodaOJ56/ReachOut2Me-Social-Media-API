from django.db import models
from django.contrib.auth.models import User


class Post(models.Model):
    # the title of the post
    title = models.CharField(max_length=200)
    # the content of the post
    content = models.TextField()
    # the image of the post
    image = models.ImageField(upload_to='post_images/', null=True, blank=True)
    # the user who wrote the post
    author = models.ForeignKey(User, on_delete=models.CASCADE)
    # the time the post was created
    created_at = models.DateTimeField(auto_now_add=True)
    # the time the post was last updated
    updated_at = models.DateTimeField(auto_now=True)
    # the users who liked the post
    likes = models.ManyToManyField(User, related_name='post_likes', blank=True)

    class Meta:
        app_label = 'ReachOut2Me'

    def __str__(self):
        return self.title


class Comment(models.Model):
    # the comment itself
    content = models.TextField()
    # the user who wrote the comment
    author = models.ForeignKey(User, on_delete=models.CASCADE)
    # the post that the comment is on
    post = models.ForeignKey(Post, on_delete=models.CASCADE)
    # the time the comment was created
    created_at = models.DateTimeField(auto_now_add=True)
    # the time the comment was last updated
    updated_at = models.DateTimeField(auto_now=True)

    class Meta:
        app_label = 'ReachOut2Me'

    def __str__(self):
        return self.content


class Message(models.Model):
    # the sender of the message
    sender = models.ForeignKey(User, on_delete=models.CASCADE, related_name='sent_messages')
    # the recipient of the message
    recipient = models.ForeignKey(User, on_delete=models.CASCADE, related_name='received_messages')
    # the content of the message
    content = models.TextField()
    # the time the message was sent
    created_at = models.DateTimeField(auto_now_add=True)

    class Meta:
        app_label = 'ReachOut2Me'

    def __str__(self):
        return self.content


class FriendRequest(models.Model):
    # the user who sent the friend request
    sender = models.ForeignKey(User, on_delete=models.CASCADE, related_name='friend_requests_sent')
    # the user who received the friend request
    recipient = models.ForeignKey(User, on_delete=models.CASCADE, related_name='friend_requests_received')
    # whether the friend request has been accepted or not
    accepted = models.BooleanField(default=False)
    # the time the friend request was sent
    created_at = models.DateTimeField(auto_now_add=True)

    class Meta:
        app_label = 'ReachOut2Me'

    def __str__(self):
        return f'{self.sender} -> {self.recipient}'
    

class UserProfile(models.Model):
    user = models.OneToOneField(User, on_delete=models.CASCADE)
    bio = models.TextField(blank=True)
    avatar = models.ImageField(blank=True, upload_to='avatars/')

    class Meta:
        app_label = 'ReachOut2Me'

    def __str__(self):
        return f"{self.user.username}'s profile"
