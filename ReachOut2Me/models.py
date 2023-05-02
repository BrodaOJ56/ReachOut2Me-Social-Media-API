from django.db import models
from django.contrib.auth.models import User


class Post(models.Model):
    # the content of the post
    content = models.CharField(max_length=280)
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
        return f"{self.author.username}'s post: {self.content}"


class Comment(models.Model):
    # the comment itself
    content = models.TextField()
    image = models.ImageField(upload_to='comment_images/', null=True, blank=True)
    # the user who wrote the comment
    author = models.ForeignKey(User, on_delete=models.CASCADE)
    # the post that the comment is on
    post = models.ForeignKey(Post, on_delete=models.CASCADE)
    # Allow users to like a comment
    likes = models.ManyToManyField(User, related_name='comment_likes', blank=True)
    # the time the comment was created
    created_at = models.DateTimeField(auto_now_add=True)
    # the time the comment was last updated
    updated_at = models.DateTimeField(auto_now=True)

    class Meta:
        app_label = 'ReachOut2Me'

    def __str__(self):
        return self.content
    

class CommentReply(models.Model):
    comment = models.ForeignKey(Comment, on_delete=models.CASCADE, related_name='commentreplies')
    user = models.ForeignKey(User, on_delete=models.CASCADE)
    reply = models.TextField()
    created_at = models.DateTimeField(auto_now_add=True)

    class Meta:
        app_label = 'ReachOut2Me'
        ordering = ['-created_at']

    def __str__(self):
        return f'Reply by {self.user.username} to {self.comment}'


class Message(models.Model):
    # the sender of the message
    sender = models.ForeignKey(User, on_delete=models.CASCADE, related_name='sent_messages')
    # the recipient of the message
    recipient = models.ForeignKey(User, on_delete=models.CASCADE, related_name='received_messages')
    # the content of the message
    content = models.TextField()
    image = models.ImageField(upload_to='message_images/', null=True, blank=True)
    # the time the message was sent
    created_at = models.DateTimeField(auto_now_add=True)

    class Meta:
        app_label = 'ReachOut2Me'

    def __str__(self):
        return self.content

    

class UserProfile(models.Model):
    user = models.OneToOneField(User, on_delete=models.CASCADE)
    following = models.ManyToManyField(User, related_name='followers_profile', blank=True)
    bio = models.TextField(null=True)
    avatar = models.ImageField(upload_to='avatars/', null=True)
    gender = models.CharField(max_length=10, null=True)
    date_of_birth = models.DateField(null=True)
    country = models.CharField(max_length=100, null=True)
    state_or_city = models.CharField(max_length=100, null=True)
    telephone_number = models.CharField(max_length=20, null=True)
    followers = models.ManyToManyField(User, related_name='following_profiles', blank=True)

    class Meta:
        app_label = 'ReachOut2Me'

    def __str__(self):
        return f"{self.user.username}'s profile"



class Follow(models.Model):
    follower = models.ForeignKey(User, on_delete=models.CASCADE, related_name='following_relationships')
    following = models.ForeignKey(User, on_delete=models.CASCADE, related_name='follower_relationships')
    created_at = models.DateTimeField(auto_now_add=True)

    class Meta:
        app_label = 'ReachOut2Me'
        unique_together = ('follower', 'following')

    def __str__(self):
        return f'{self.follower.username} follows {self.following.username}'



class Notification(models.Model):
    # the user who the notification is for
    user = models.ForeignKey(User, on_delete=models.CASCADE)
    # the content of the notification
    content = models.TextField()
    # whether the notification has been read or not
    read = models.BooleanField(default=False)
    # the time the notification was created
    created_at = models.DateTimeField(auto_now_add=True)

    class Meta:
        app_label = 'ReachOut2Me'

    def __str__(self):
        return self.content
