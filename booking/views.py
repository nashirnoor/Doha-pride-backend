from rest_framework import viewsets
from .models import TourBooking,TransferBooking
from .serializers import BookingSerializer,TransferBookingSerializer

class BookingViewSet(viewsets.ModelViewSet):
    queryset = TourBooking.objects.all()
    serializer_class = BookingSerializer

class BookingTransferViewSet(viewsets.ModelViewSet):
    queryset = TransferBooking.objects.all()
    serializer_class = TransferBookingSerializer