from django.shortcuts import render

# Create your views here.


from rest_framework import viewsets
from .models import Booking,TransferBooking
from .serializers import BookingSerializer,TransferBookingSerializer

class BookingViewSet(viewsets.ModelViewSet):
    queryset = Booking.objects.all()
    serializer_class = BookingSerializer


class BookingTransferViewSet(viewsets.ModelViewSet):
    queryset = TransferBooking.objects.all()
    serializer_class = TransferBookingSerializer