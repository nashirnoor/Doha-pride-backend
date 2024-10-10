from rest_framework import generics
from .models import Statistic, Activity,Description
from .serializers import StatisticSerializer, ActivitySerializer,DescriptionSerializer

class StatisticListCreateAPIView(generics.ListCreateAPIView):
    queryset = Statistic.objects.all()
    serializer_class = StatisticSerializer

class ActivityListCreateAPIView(generics.ListCreateAPIView):
    queryset = Activity.objects.all()
    serializer_class = ActivitySerializer

class DescriptionDetailView(generics.RetrieveAPIView):
    queryset = Description.objects.all()
    serializer_class = DescriptionSerializer