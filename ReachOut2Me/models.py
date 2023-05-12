from django.db import models
from django.contrib.auth.models import User
from django.contrib.contenttypes.models import ContentType
from django.contrib.contenttypes.fields import GenericForeignKey
from django.db import models
from django.utils import timezone
from django.urls import reverse
from django.conf import settings


class Post(models.Model):
    # the content of the post
    content = models.CharField(max_length=280)
    # the image of the post
    image = models.ImageField(upload_to='post_images/', null=True, blank=True)
    # the user who wrote the post
    user = models.ForeignKey(User, on_delete=models.CASCADE)
    # the time the post was created
    created_at = models.DateTimeField(auto_now_add=True)
    # the time the post was last updated
    updated_at = models.DateTimeField(auto_now=True)
    # the users who liked the post
    likes = models.ManyToManyField(User, related_name='post_likes', blank=True)

    class Meta:
        app_label = 'ReachOut2Me'

    def __str__(self):
        return f"{self.user.username}'s post: {self.content}"


class Comment(models.Model):
    # the comment itself
    content = models.TextField()
    image = models.ImageField(upload_to='comment_images/', null=True, blank=True)
    # the user who wrote the comment
    user = models.ForeignKey(User, on_delete=models.CASCADE)
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
    
class CommentReplyLike(models.Model):
    user = models.ForeignKey(User, on_delete=models.CASCADE)  # The user who liked the comment reply
    comment_reply = models.ForeignKey(CommentReply, on_delete=models.CASCADE, related_name='likes')  # The comment reply that was liked
    created_at = models.DateTimeField(auto_now_add=True)  # The timestamp when the like was created

    class Meta:
        app_label = 'ReachOut2Me'
        unique_together = ('user', 'comment_reply')  # A user can only like a comment reply once

    def __str__(self):
        return f"{self.user.username} liked {self.comment_reply}"  # String representation of the object```




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
    NOTIFICATION_TYPES = (
        ("follow", "Follow"),
        ("message", "Message"),
        ("post_like", "Post Like"),
        ("comment", "Comment"),
        ("comment_like", "Comment Like"),
        ("reply", "Reply"),
        ("reply_like", "Reply"),
    )

    recipient = models.ForeignKey(settings.AUTH_USER_MODEL, on_delete=models.CASCADE)
    actor_content_type = models.ForeignKey(ContentType, on_delete=models.CASCADE, related_name="notify_actor", null=True, blank=True)
    actor_object_id = models.PositiveIntegerField(default=0)
    actor_object = GenericForeignKey('actor_content_type', 'actor_object_id')
    verb = models.CharField(max_length=255, choices=NOTIFICATION_TYPES, default='follow')
    read = models.BooleanField(default=False)
    timestamp = models.DateTimeField(default=timezone.now)

    def __str__(self):
        return f"{self.recipient.username} {self.verb}"

    def get_absolute_url(self):
        if self.verb == "follow":
            return reverse("user_detail", kwargs={"username": self.actor_object.username})
        elif self.verb == "message":
            return reverse("messages")
        elif self.verb == "post_like":
            return reverse("post_detail", kwargs={"pk": self.actor_object.pk})
        elif self.verb == "comment_like":
            return reverse("comment_detail", kwargs={"pk": self.actor_object.pk})
        elif self.verb == "comment":
            return reverse("post_detail", kwargs={"pk": self.actor_object.post.pk})
        elif self.verb == "reply":
            return reverse("post_detail", kwargs={"pk": self.actor_object.post.pk})
        elif self.verb == "reply_like":
            return reverse("comment_detail", kwargs={"pk": self.actor_object.parent_comment.pk})

            
    @classmethod
    def create_message_notification(cls, recipient, message):
        actor_content_type = ContentType.objects.get_for_model(message.sender)
        notification = cls.objects.create(
            recipient=recipient,
            actor_content_type=actor_content_type,
            actor_object_id=message.sender.id,
            verb='message'
        )
        return notification
    
    @classmethod
    def create_follow_notification(cls, recipient, actor):
        actor_content_type = ContentType.objects.get_for_model(actor)
        notification = cls.objects.create(
            recipient=recipient,
            actor_content_type=actor_content_type,
            actor_object_id=actor.id,
            verb='follow'
        )
        return notification
    
    @classmethod
    def create_post_like_notification(cls, recipient, post, actor):
        actor_content_type = ContentType.objects.get_for_model(actor)
        notification = cls.objects.create(
            recipient=recipient,
            actor_content_type=actor_content_type,
            actor_object_id=actor.id,
            verb='post_like',
            actor_object=post
        )
        return notification
    
    @classmethod
    def create_comment_notification(cls, recipient, comment, actor):
        actor_content_type = ContentType.objects.get_for_model(actor)
        notification = cls.objects.create(
            recipient=recipient,
            actor_content_type=actor_content_type,
            actor_object_id=actor.id,
            verb='comment',
            actor_object=comment
        )
        return notification
    
    @classmethod
    def create_comment_like_notification(cls, recipient, comment, actor):
        actor_content_type = ContentType.objects.get_for_model(actor)
        notification = cls.objects.create(
            recipient=recipient,
            actor_content_type=actor_content_type,
            actor_object_id=actor.id,
            verb='comment_like',
            actor_object=comment
        )
        return notification
    
    @classmethod
    def create_reply_notification(cls, recipient, reply, actor):
        actor_content_type = ContentType.objects.get_for_model(actor)
        notification = cls.objects.create(
            recipient=recipient,
            actor_content_type=actor_content_type,
            actor_object_id=actor.id,
            verb='reply',
            actor_object=reply.comment
        )
        return notification
    
    @classmethod
    def reply_like_notification(cls, recipient, reply_like):
        actor_content_type = ContentType.objects.get_for_model(reply_like.user)
        notification = cls.objects.create(
            recipient=recipient,
            actor_content_type=actor_content_type,
            actor_object_id=reply_like.user.id,
            verb='reply_like',
            actor_object=reply_like
        )
        return notification
    

