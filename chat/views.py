from rest_framework import generics
from rest_framework.permissions import IsAuthenticated
from .models import ChatRoom, Message
from .serializers import ChatRoomSerializer, MessageSerializer
from django.db import models
from django.db.models import Q 

class ChatRoomListCreateView(generics.ListCreateAPIView):
    serializer_class = ChatRoomSerializer
    permission_classes = [IsAuthenticated]

    def get_queryset(self):
        user = self.request.user
        if user.user_type == 'driver':
            return ChatRoom.objects.filter(driver=user)
        return ChatRoom.objects.filter(customer=user)

class MessageListCreateView(generics.ListCreateAPIView):
    serializer_class = MessageSerializer
    permission_classes = [IsAuthenticated]

    def get_queryset(self):
        user = self.request.user
        return Message.objects.filter(
            models.Q(sender=user) | models.Q(receiver=user)
        ).order_by('-created_at')

class ChatRoomMessagesView(generics.ListAPIView):
    serializer_class = MessageSerializer
    permission_classes = [IsAuthenticated]

    def get_queryset(self):
        other_user_id = self.kwargs['pk']  # This could be either driver_id or customer_id
        current_user = self.request.user

        chat_room = ChatRoom.objects.filter(
            (Q(driver=current_user) & Q(customer_id=other_user_id)) |
            (Q(customer=current_user) & Q(driver_id=other_user_id))
        ).first()

        if chat_room:
            Message.objects.filter(
                chat_room=chat_room,
                receiver=current_user,
                status='unread'
            ).update(status='read')
            
            return Message.objects.filter(chat_room=chat_room).order_by('created_at')
        return Message.objects.none()