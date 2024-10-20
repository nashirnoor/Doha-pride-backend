from rest_framework import viewsets
from .models import TourBooking,TransferBooking
from .serializers import BookingSerializer,TransferBookingSerializer
from django.views.decorators.csrf import csrf_exempt
from django.utils.decorators import method_decorator
from rest_framework.permissions import AllowAny
from rest_framework_simplejwt.authentication import JWTAuthentication
from rest_framework.response import Response
from rest_framework.decorators import action

class BookingViewSet(viewsets.ModelViewSet):
    queryset = TourBooking.objects.all()
    serializer_class = BookingSerializer

@method_decorator(csrf_exempt, name='dispatch')
class BookingTransferViewSet(viewsets.ModelViewSet):
    authentication_classes = [JWTAuthentication]
    permission_classes = [AllowAny]
    serializer_class = TransferBookingSerializer

    def get_queryset(self):
        user_email = self.request.query_params.get('email', None)
        if user_email:
            return TransferBooking.objects.filter(email=user_email)
        return TransferBooking.objects.all()
    
    def perform_create(self, serializer):
        user_email = self.request.user.email if self.request.user.is_authenticated else None
        serializer.save(email=user_email)

    @action(detail=False, methods=['get'])
    def user_bookings(self, request):
        email = request.query_params.get('email', None)
        if email:
            bookings = TransferBooking.objects.filter(email=email).select_related('driver', 'transfer_name')
            serializer = self.get_serializer(bookings, many=True)
            return Response(serializer.data)
        return Response({'error': 'Email parameter is required'}, status=400)