from .endpoints.users import *
from .endpoints.auth import *
from django.urls import path
from .endpoints.posts import PostListCreateView, PostDetailView, PostLikeView, CreateGetComment, UpdateDeleteComment

urlpatterns = [
    path('users/', GetAllUsers.as_view(), name='get_all_users'),
    path('register/', RegisterUser.as_view(), name='register_user'),
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
    # allows users to login
    path('login/', LoginView.as_view(), name='login_user'),
]
