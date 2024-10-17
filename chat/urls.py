from django.urls import path
from . import views

urlpatterns = [
    path('chat-rooms/', views.ChatRoomListCreateView.as_view()),
    path('messages/', views.MessageListCreateView.as_view()),
    path('chat-rooms/<int:pk>/messages/', views.ChatRoomMessagesView.as_view()),
]