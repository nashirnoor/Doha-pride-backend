from rest_framework import generics
from .models import BackgroundVideo, CardOne, CardTwo
from .serializers import BackgroundVideoSerializer, CardOneSerializer, CardTwoSerializer

class BackgroundVideoListView(generics.ListAPIView):
    queryset = BackgroundVideo.objects.all()
    serializer_class = BackgroundVideoSerializer

class CardOneListView(generics.ListAPIView):
    queryset = CardOne.objects.all()
    serializer_class = CardOneSerializer

class CardTwoListView(generics.ListAPIView):
    queryset = CardTwo.objects.all()
    serializer_class = CardTwoSerializer
