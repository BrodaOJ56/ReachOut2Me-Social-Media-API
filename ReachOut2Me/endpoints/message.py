from rest_framework import generics
from ..models import Message, Notification
from ..serializers import MessageSerializer
from drf_spectacular.utils import extend_schema

"""
This code defines an API endpoint that allows users to view and create messages through HTTP requests. 
The `queryset` attribute determines the list of messages that will be displayed on the API endpoint, 
while the `serializer_class` attribute specifies the serializer that will be used to serialize and deserialize data. 
The `perform_create` method is used to save the message object with the authenticated sender as the message sender. 
This ensures that the sender's identity is properly associated with the message object in the database.
"""


class MessageList(generics.ListCreateAPIView):
    queryset = Message.objects.all()
    serializer_class = MessageSerializer

    @extend_schema(
        tags=['Message']
    )
    def perform_create(self, serializer):
        message = serializer.save(sender=self.request.user)
        Notification.create(user=message.recipient,
                            content=f'You have a new message from {message.sender.username}',
                            category='message')


"""
This code enables retrieving and creating a specific instance of a `Message` model. 
The `queryset` attribute determines the list of messages that can be retrieved, 
while the `serializer_class` attribute specifies the serializer responsible for serializing 
and deserializing message objects. 
"""


class MessageDetail(generics.RetrieveUpdateDestroyAPIView):
    queryset = Message.objects.all()
    serializer_class = MessageSerializer

    @extend_schema(
        tags=['Message']
    )
    def perform_create(self, serializer):
        serializer.save(sender=self.request.user)
