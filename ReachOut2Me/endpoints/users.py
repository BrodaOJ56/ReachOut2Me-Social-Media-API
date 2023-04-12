from ..models import User, UserProfile
from rest_framework.views import APIView
from rest_framework.response import Response
from rest_framework import status


# Just testing out the APIView for the get all users endpoint
class GetAllUsers(APIView):
    def get(self, request):
        users = User.objects.select_related('userprofile').all()
        all_users = []
        for user in users:
            if user.email:
                user.email = user.email
            else:
                user.email = 'No email provided'
            all_users.append({
                'username': user.username,
                'email': user.email,
                'is_staff': user.is_staff,
                'is_active': user.is_active,
                'is_superuser': user.is_superuser,
                'date_joined': user.date_joined,
                'last_login': user.last_login,
                'bio': user.userprofile.bio if hasattr(user, 'userprofile') else 'No bio available',
            })
        return Response(all_users, status=status.HTTP_200_OK)


# Endpoint to register as a new user
class RegisterUser(APIView):
    def post(self, request):
        data = request.data
        required_fields = ['username', 'password', 'first_name', 'last_name', 'email']
        if not all(field in data for field in required_fields):
            return Response({'error': 'Username, password, first name, last name, and email are required.'},
                            status=status.HTTP_400_BAD_REQUEST)
        user = User.objects.create_user(**data)
        return Response({'success': f'User {user.username} registered.'}, status=status.HTTP_201_CREATED)
