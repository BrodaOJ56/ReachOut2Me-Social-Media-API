from rest_framework import generics
from ..models import Message
from ..serializers import MessageSerializer

class MessageList(generics.ListCreateAPIView):
    queryset = Message.objects.all()
    serializer_class = MessageSerializer

    def perform_create(self, serializer):
        serializer.save(sender=self.request.user)

class MessageDetail(generics.RetrieveUpdateDestroyAPIView):
    queryset = Message.objects.all()
    serializer_class = MessageSerializer

    def perform_create(self, serializer):
        serializer.save(sender=self.request.user)
