from django.contrib import admin

from .models import Post, Comment, Message, FriendRequest, UserProfile

# registered models with the admin site

admin.site.register(Post)
admin.site.register(Comment)
admin.site.register(Message)
admin.site.register(FriendRequest)
admin.site.register(UserProfile)
