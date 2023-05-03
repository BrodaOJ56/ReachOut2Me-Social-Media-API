from ..models import Notification
from ..serializers import NotificationSerializer
from rest_framework.response import Response
from rest_framework.views import APIView
from .message import
from django.shortcuts import redirect


class NotificationList(APIView):
    def get(self, request, *args, **kwargs):
        user = request.user
        notifications = Notification.objects.filter(user=user)
        serializer = NotificationSerializer(notifications, many=True)
        return Response(serializer.data)


class GetNotificationByCategory(APIView):
    def get(self, request, *args, **kwargs):
        user = request.user
        category = kwargs.get('category')
        if category == 'comment':
            post = kwargs.get('post')
            return redirect(f'/api/posts/{post}/')

