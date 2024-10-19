from rest_framework import viewsets
from .models import TourBooking,TransferBooking
from .serializers import BookingSerializer,TransferBookingSerializer
from django.views.decorators.csrf import csrf_exempt
from django.utils.decorators import method_decorator
from rest_framework.permissions import AllowAny
from rest_framework_simplejwt.authentication import JWTAuthentication


class BookingViewSet(viewsets.ModelViewSet):
    queryset = TourBooking.objects.all()
    serializer_class = BookingSerializer


@method_decorator(csrf_exempt, name='dispatch')
class BookingTransferViewSet(viewsets.ModelViewSet):
    authentication_classes = [JWTAuthentication]
    permission_classes = [AllowAny]
    queryset = TransferBooking.objects.all()
    serializer_class = TransferBookingSerializer
    
    def perform_create(self, serializer):
        user_email = self.request.user.email if self.request.user.is_authenticated else None
        serializer.save(email=user_email)