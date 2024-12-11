from rest_framework import serializers
from .models import ChatMessage
from driver.serializers import UserSerializer
class ChatMessageSerializer(serializers.ModelSerializer):
    sender = UserSerializer(read_only=True)
    
    class Meta:
        model = ChatMessage
        fields = ['id', 'sender', 'receiver', 'message', 'timestamp', 'is_read']
        extra_kwargs = {
            'receiver': {'required': True},
            'message': {'required': True}
        }