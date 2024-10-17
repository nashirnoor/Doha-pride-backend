from django.db import models
from django.contrib.auth import get_user_model

User = get_user_model()

class ChatRoom(models.Model):
    driver = models.ForeignKey(User, on_delete=models.CASCADE, related_name='driver_chats')
    customer = models.ForeignKey(User, on_delete=models.CASCADE, related_name='customer_chats')
    created_at = models.DateTimeField(auto_now_add=True)

    class Meta:
        unique_together = ('driver', 'customer')

class Message(models.Model):
    CONTENT_TYPES = (
        ('text', 'Text'),
        ('image', 'Image'),
    )
    STATUS_CHOICES = (
        ('read', 'Read'),
        ('unread', 'Unread'),
    )

    chat_room = models.ForeignKey(ChatRoom, on_delete=models.CASCADE, related_name='messages')
    sender = models.ForeignKey(User, on_delete=models.CASCADE, related_name='sent_messages')
    receiver = models.ForeignKey(User, on_delete=models.CASCADE, related_name='received_messages')
    content_type = models.CharField(max_length=5, choices=CONTENT_TYPES, default='text')
    content = models.TextField()
    sub_content = models.JSONField(null=True, blank=True)
    is_reply = models.BooleanField(default=False)
    replied_message = models.ForeignKey('self', null=True, blank=True, on_delete=models.SET_NULL)
    status = models.CharField(max_length=6, choices=STATUS_CHOICES, default='unread')
    created_at = models.DateTimeField(auto_now_add=True)