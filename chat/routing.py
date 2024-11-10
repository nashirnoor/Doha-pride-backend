from django.urls import path

from .import consumers
from django.urls import re_path

websocket_urlpatterns = [
    re_path(r'ws/chat/$', consumers.ChatConsumer.as_asgi()),
    re_path(r'', consumers.ChatConsumer.as_asgi()),

]