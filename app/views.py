# views.py
from rest_framework import generics
from .models import TransferMeetAssist
from .serializers import TransferMeetAssistSerializer

class TransferMeetAssistList(generics.ListCreateAPIView):
    queryset = TransferMeetAssist.objects.all()
    serializer_class = TransferMeetAssistSerializer

class TransferMeetAssistDetail(generics.RetrieveUpdateDestroyAPIView):
    queryset = TransferMeetAssist.objects.all()
    serializer_class = TransferMeetAssistSerializer