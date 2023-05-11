from django.shortcuts import get_object_or_404
from django.http import JsonResponse
from django.contrib.auth.decorators import login_required
from django.views.decorators.http import require_POST
from drf_spectacular.utils import extend_schema
from rest_framework.decorators import api_view
from ..models import Notification
from ..serializers import NotificationSerializer

@api_view(['GET'])
@login_required
@extend_schema(
    description='Get a list of notifications for the authenticated user.',
    responses={
        200: NotificationSerializer(many=True),
        401: 'Unauthorized',
    },
)
def list_notifications(request):
    print('list_notifications view called')
    notifications = Notification.objects.filter(recipient=request.user).order_by('-timestamp')
    Notification.objects.filter(recipient=request.user, read=False).update(read=True)
    serializer = NotificationSerializer(notifications, many=True)
    return JsonResponse(serializer.data, safe=False)

@api_view(['POST'])
@login_required
@extend_schema(
    description='Delete a notification for the authenticated user.',
    responses={
        200: {'status': 'ok'},
        401: 'Unauthorized',
        404: 'Not Found',
        403: 'Forbidden',
    },
)
def delete_notification(request, notification_id):
    print('delete_notification view called')
    notification = get_object_or_404(Notification, id=notification_id)
    if notification.recipient != request.user:
        return JsonResponse({'status': 'error', 'message': 'You are not authorized to delete this notification.'}, status=403)
    notification.delete()
    return JsonResponse({'status': 'ok'})
