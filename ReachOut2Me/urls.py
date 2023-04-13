from .endpoints.users import GetAllUsers, RegisterUser, UserProfileView
from django.urls import path

urlpatterns = [
    path('users/', GetAllUsers.as_view(), name='get_all_users'),
    path('register/', RegisterUser.as_view(), name='register_user'),
    path('profile/', UserProfileView.as_view(), name='user_profile'),
]
