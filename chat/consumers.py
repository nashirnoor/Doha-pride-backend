from channels.generic.websocket import WebsocketConsumer
from asgiref.sync import async_to_sync
import json

class ChatConsumer(WebsocketConsumer):
    def connect(self):
        user = self.scope['user']
        print(user,user.is_authenticated)
        if not user.is_authenticated:
            return
        self.username = user.username
        async_to_sync(self.channel_layer.group_add)(
            self.username, self.channel_name
        )
        self.accept()

    def disconnect(self, close_code):
        async_to_sync(self.channel_layer.group_discard)(
            self.username, self.channel_name
        )

    def receive(self, text_data):
        data = json.load(text_data)
        data_source = data.get('source')
        print('receive', json.dumps(data, index=2))