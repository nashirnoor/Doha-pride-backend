from rest_framework import serializers
from .models import Message, ChatRoom

class MessageSerializer(serializers.ModelSerializer):
    sender = serializers.SerializerMethodField()
    receiver = serializers.SerializerMethodField()

    class Meta:
        model = Message
        fields = ['id', 'content', 'content_type', 'created_at', 'sender', 'receiver', 'status']

    def get_sender(self, obj):
        return {
            'id': str(obj.sender.id),  
            'username': obj.sender.username,
            'user_type': obj.sender.user_type
        }

    def get_receiver(self, obj):
        return {
            'id': str(obj.receiver.id),  
            'username': obj.receiver.username,
            'user_type': obj.receiver.user_type
        }

class ChatRoomSerializer(serializers.ModelSerializer):
    class Meta:
        model = ChatRoom
        fields = '__all__'