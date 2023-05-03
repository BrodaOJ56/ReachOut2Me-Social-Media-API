from .endpoints.users import *
from .endpoints.auth import *
from django.urls import path
from .endpoints.posts import PostListCreateView, PostDetailView, PostLikeView, CreateGetComment, UpdateDeleteComment, CommentLike, UpdateDeleteCommentReply, ListCreateCommentReply
from .endpoints.message import MessageList, MessageDetail
from .endpoints.followers import follow_user, unfollow_user,followers_list
from .endpoints.notification import NotificationList

urlpatterns = [
    # get all users
    path('users/', GetAllUsers.as_view(), name='get_all_users'),
    # register a user
    path('register/', RegisterUser.as_view(), name='register_user'),
    # view user profile
    path('profile/', UserProfileView.as_view(), name='user_profile'),
    # path('avatar/<str:first_name>/<str:last_name>/', UploadAvatarView.as_view(), name='user_avatar'),
    path('avatar/', UploadAvatarView.as_view(), name='user_avatar'),
    # path('avatar/<string:first_name>/<string:last_name>/', UploadAvatarView.as_view(), name='user_avatar'),
    # retrieve a list of posts or create a new post by sending a POST request with the required data in the request body
    path('posts/', PostListCreateView.as_view(), name='post_list_create'),
    # allows users to retrieve a single post using the GET method and update using PUT method
    path('posts/<int:pk>/', PostDetailView.as_view(), name='post_detail'),
    # allows users to retrieve a single post and like/unlike post using POST method
    path('posts/<int:pk>/like/', PostLikeView.as_view(), name='post_like'),
    # allows users to create and retrieve comment by ID
    path('posts/<int:post_id>/comments/', CreateGetComment.as_view(), name='create-comment'),
    # allows users to update and delete comment by ID
    path('posts/<int:post_id>/comments/<int:comment_id>/', UpdateDeleteComment.as_view(), name='update-comment'),
    # allows users to like/unlike comment by ID
    path('comments/<int:comment_id>/like/', CommentLike.as_view(), name='comment_like'),
    # allows users to reply a comment and view all comment replies
    path('comments/<int:comment_id>/replies/', ListCreateCommentReply.as_view(), name='create_get_comment_reply'),
    # allows users to update and delete reply
    path('comments/<int:comment_id>/replies/<int:reply_id>/', UpdateDeleteCommentReply.as_view(), name='update_delete_comment_reply'),
    # allows users to login
    path('login/', LoginView.as_view(), name='login_user'),
    # get current user
    path('my_account/', GetUserProfile.as_view(), name='get_user_profile'),
    # logout user
    path('logout/', LogoutView.as_view(), name='logout_user'),
    # search for user by username
    path('search/<slug:username>/', SearchUserView.as_view(), name='search_user'),
    # allow users to create message and get message
    path('messages/', MessageList.as_view(), name='message-list'),
    # allow users to view message by id
    path('messages/<int:pk>/', MessageDetail.as_view(), name='message-detail'),
    # follow user
    path('user/<int:user_id>/follow/', follow_user, name='follow_user'),
    # unfollow user
    path('user/<int:user_id>/unfollow/', unfollow_user, name='unfollow_user'),
    # list followers
    path('users/<int:user_id>/followers/', followers_list, name='followers_list'),
    # list notifications
    path('notifications/', NotificationList.as_view(), name='notification_list'),

]
