from .endpoints.users import GetAllUsers, RegisterUser
from django.urls import path

urlpatterns = [
    path('users', GetAllUsers.as_view(), name='get_all_users'),
    path('register', RegisterUser.as_view(), name='register_user'),
]
