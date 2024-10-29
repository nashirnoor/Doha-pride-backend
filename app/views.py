# views.py
from rest_framework import generics
from .models import TransferMeetAssist
from .serializers import TransferMeetAssistSerializer
from rest_framework.permissions import AllowAny

class TransferMeetAssistList(generics.ListCreateAPIView):
    permission_classes = [AllowAny]
    queryset = TransferMeetAssist.objects.all()
    serializer_class = TransferMeetAssistSerializer

class TransferMeetAssistDetail(generics.RetrieveUpdateDestroyAPIView):
    queryset = TransferMeetAssist.objects.all()
    serializer_class = TransferMeetAssistSerializer