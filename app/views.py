# views.py
from rest_framework import generics
from .models import TransferMeetAssist,HomeBanner
from .serializers import TransferMeetAssistSerializer,BannerSerializer
from rest_framework.permissions import AllowAny
from rest_framework.response import Response
from rest_framework.views import APIView
from rest_framework import status


class TransferMeetAssistList(generics.ListCreateAPIView):
    permission_classes = [AllowAny]
    queryset = TransferMeetAssist.objects.all()
    serializer_class = TransferMeetAssistSerializer

# class TransferMeetAssistDetail(generics.RetrieveUpdateDestroyAPIView):
#     queryset = TransferMeetAssist.objects.all()
#     serializer_class = TransferMeetAssistSerializer


class HomeBannerListView(APIView):
    permission_classes =[AllowAny]
    def get(self, request):
        banners = HomeBanner.objects.all()
        serializer = BannerSerializer(banners, many=True)
        return Response(serializer.data, status=status.HTTP_200_OK)