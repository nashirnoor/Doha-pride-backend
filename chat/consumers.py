import json
from channels.generic.websocket import WebsocketConsumer
from channels.db import database_sync_to_async
from asgiref.sync import async_to_sync
from .models import Message, ChatRoom
from .serializers import MessageSerializer
from django.contrib.auth import get_user_model
import uuid

User = get_user_model()

class ChatConsumer(WebsocketConsumer):
    def connect(self):
        user = self.scope['user']
        if user.is_authenticated:
            self.username = user.username
        else:
            # Generate temporary ID for guest user
            self.username = f"guest_{uuid.uuid4().hex[:8]}"
        
        if self.channel_layer is not None:
            async_to_sync(self.channel_layer.group_add)(
                self.username, self.channel_name
            )
            # Add to admin group to receive messages
            async_to_sync(self.channel_layer.group_add)(
                'admin_support', self.channel_name
            )
        self.accept()

    

    def disconnect(self, close_code):
        if self.channel_layer is not None:
            async_to_sync(self.channel_layer.group_discard)(
                self.username, self.channel_name
            )

    @database_sync_to_async
    def get_or_create_chat_room(self, driver_id, customer_id):
        driver = User.objects.get(id=driver_id)
        customer = User.objects.get(id=customer_id)
        chat_room, created = ChatRoom.objects.get_or_create(
            driver=driver,
            customer=customer
        )
        return chat_room

    @database_sync_to_async
    def save_message(self, data, chat_room):
        sender = User.objects.get(username=self.username)
        if sender.user_type == 'driver':
            receiver = chat_room.customer
        else:
            receiver = chat_room.driver

        message = Message.objects.create(
            chat_room=chat_room,
            sender=sender,
            receiver=receiver,
            content_type=data['content_type'],
            content=data['content'],
            sub_content=data.get('subContent'),
            is_reply=data.get('isReply', False),
            status='unread'
        )

        if data.get('isReply') and data.get('repliedMessage'):
            replied_msg = Message.objects.get(id=data['repliedMessage'])
            message.replied_message = replied_msg
            message.save()

        return message

    def receive(self, text_data):
        try:
            data = json.loads(text_data)
            source = data.get('source')
            print(f"Received data: {data}")  

            if source == 'support_chat':
                # Handle support chat messages
                message = async_to_sync(self.save_support_message)(data)
                serialized_message = MessageSerializer(message).data

                # Send to admin group
                async_to_sync(self.channel_layer.group_send)(
                    'admin_support',
                    {
                        'type': 'chat_message',
                        'message': serialized_message
                    }
                )

            if source == 'chat':
                if 'driver_id' not in data or 'customer_id' not in data:
                    raise ValueError("Missing required fields: driver_id and customer_id")

                chat_room = async_to_sync(self.get_or_create_chat_room)(
                    data['driver_id'],
                    data['customer_id']
                )

                message = async_to_sync(self.save_message)(data, chat_room)
                serialized_message = MessageSerializer(message).data

                async_to_sync(self.channel_layer.group_send)(
                    message.receiver.username,
                    {
                        'type': 'chat_message',
                        'message': serialized_message
                    }
                )
        except json.JSONDecodeError as e:
            print(f"JSON decode error: {e}")
            self.send(text_data=json.dumps({
                'error': 'Invalid JSON format'
            }))
        except KeyError as e:
            print(f"Missing required field: {e}")
            self.send(text_data=json.dumps({
                'error': f'Missing required field: {str(e)}'
            }))
        except Exception as e:
            print(f"Error processing message: {e}")
            self.send(text_data=json.dumps({
                'error': str(e)
            }))

    def chat_message(self, event):
        message = event['message']
        self.send(text_data=json.dumps({
            'source': 'chat',
            'message': message
        }))