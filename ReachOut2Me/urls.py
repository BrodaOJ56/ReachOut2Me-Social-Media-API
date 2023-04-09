from .endpoints.users import GetAllUsers
from django.urls import path

urlpatterns = [
    path('', GetAllUsers.as_view(), name='get_all_users'),
]
