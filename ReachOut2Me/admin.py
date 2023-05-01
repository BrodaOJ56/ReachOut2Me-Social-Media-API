from django.contrib import admin

from .models import Post, Comment, Message, UserProfile,CommentReply,Notification, Follow

# registered models with the admin site

admin.site.register(Post)
admin.site.register(Comment)
admin.site.register(Message)
admin.site.register(UserProfile)
admin.site.register(CommentReply)
admin.site.register(Notification)
admin.site.register(Follow)
