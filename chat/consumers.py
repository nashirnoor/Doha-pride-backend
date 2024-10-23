import json
from channels.generic.websocket import WebsocketConsumer
from channels.db import database_sync_to_async
from asgiref.sync import async_to_sync
from .models import Message, ChatRoom
from .serializers import MessageSerializer
from django.contrib.auth import get_user_model

User = get_user_model()

class ChatConsumer(WebsocketConsumer):
    def connect(self):
        user = self.scope['user']
        if not user.is_authenticated:
            return
        self.username = user.username
        if self.channel_layer is not None:
            async_to_sync(self.channel_layer.group_add)(
                self.username, self.channel_name
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
    def get_or_create_admin_driver_chat(self, driver_id, admin_id):
        driver = User.objects.get(id=driver_id)
        admin = User.objects.get(id=admin_id)
        chat_room, created = ChatRoom.objects.get_or_create(
            driver=driver,
            admin=admin,
            customer=None
        )
        return chat_room

    @database_sync_to_async
    def save_message(self, data, chat_room):
        sender = User.objects.get(username=self.username)
        # Determine receiver based on sender's type and chat room
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

            if source == 'chat':
                if 'driver_id' in data and 'admin_id' in data:
                    # Admin-Driver chat
                    chat_room = async_to_sync(self.get_or_create_admin_driver_chat)(
                        data['driver_id'],
                        data['admin_id']
                    )
                elif 'driver_id' in data and 'customer_id' in data:
                    # Customer-Driver chat
                    chat_room = async_to_sync(self.get_or_create_chat_room)(
                        data['driver_id'],
                        data['customer_id']
                    )
                else:
                    raise ValueError("Missing required fields")

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