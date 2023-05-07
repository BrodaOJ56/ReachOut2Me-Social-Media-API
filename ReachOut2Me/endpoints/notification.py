from ..models import Notification
from ..serializers import NotificationSerializer
from rest_framework.response import Response
from rest_framework.views import APIView
from django.shortcuts import redirect
from drf_spectacular.utils import extend_schema



@extend_schema(
    request=NotificationSerializer,
        responses=None ,
        tags=['notifications']
    )
class NotificationList(APIView):
    
    def get(self, request, *args, **kwargs):
        user = request.user
        notifications = Notification.objects.filter(user=user)
        serializer = NotificationSerializer(notifications, many=True)
        return Response(serializer.data)


class GetNotificationByCategory(APIView):
    @extend_schema(
        tags=['notifications']
    )
    def get(self, request, *args, **kwargs):
        user = request.user
        category = kwargs.get('category')
        if category == 'comment':
            post = kwargs.get('post')
            return redirect(f'/api/posts/{post}/')
        elif category == 'message':
            pass
        elif category == 'reply':
            pass
        elif category == 'follow':
            pass
        elif category == 'like':
            pass
