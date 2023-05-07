from rest_framework.decorators import api_view, permission_classes
from rest_framework.permissions import IsAuthenticated
from rest_framework.response import Response
from rest_framework import status
from ..models import Message
from ..serializers import MessageSerializer
from drf_spectacular.utils import extend_schema

"""
This code defines an API endpoint that allows users to view and create messages through HTTP requests. 
The `queryset` attribute determines the list of messages that will be displayed on the API endpoint, 
while the `serializer_class` attribute specifies the serializer that will be used to serialize and deserialize data. 
The `perform_create` method is used to save the message object with the authenticated sender as the message sender. 
This ensures that the sender's identity is properly associated with the message object in the database.
"""

@extend_schema(request=MessageSerializer,
        responses={200: None},
        tags=['Message']
    )
@api_view(['POST'])
def send_message(request):
    """
    Endpoint for sending a message.
    """
    serializer = MessageSerializer(data=request.data)
    if serializer.is_valid():
        serializer.save(sender=request.user)
        return Response(serializer.data, status=status.HTTP_201_CREATED)
    return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)

@extend_schema(request=None,
        responses={200: MessageSerializer},
        tags=['Message']
    )
@api_view(['GET'])
def message_list(request):
    """
    Retrieve all messages sent and received by the current user.
    """
    # Get the current user
    user = request.user

    # Get all messages sent and received by the user
    messages = Message.objects.filter(sender=user) | Message.objects.filter(recipient=user)

    # Serialize the messages
    serializer = MessageSerializer(messages, many=True)

    # Return the serialized messages as a JSON response
    return Response(serializer.data, status=status.HTTP_200_OK)


"""
This code enables retrieving and creating a specific instance of a `Message` model. 
The `queryset` attribute determines the list of messages that can be retrieved, 
while the `serializer_class` attribute specifies the serializer responsible for serializing 
and deserializing message objects. 
"""
@permission_classes([IsAuthenticated])
@extend_schema(request=None,
        responses={200: MessageSerializer},
        tags=['Message']
    )
@api_view(['GET'])
def message_detail(request, message_id):
    try:
        message = Message.objects.get(id=message_id)
    except Message.DoesNotExist:
        return Response({"error": "Message not found"}, status=status.HTTP_404_NOT_FOUND)
    
    # Check if the user is either the sender or the recipient of the message
    if message.sender != request.user and message.recipient != request.user:
        return Response({"error": "You are not authorized to view this message"}, status=status.HTTP_403_FORBIDDEN)
    
    serializer = MessageSerializer(message)
    return Response(serializer.data, status=status.HTTP_200_OK)

