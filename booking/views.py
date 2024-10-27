from rest_framework import viewsets
from .models import TourBooking,TransferBooking,TransferBookingAudit
from .serializers import BookingSerializer,TransferBookingSerializer,TransferBookingAuditSerializer,DriverTransferBookingSerializer
from django.views.decorators.csrf import csrf_exempt
from django.utils.decorators import method_decorator
from rest_framework.permissions import AllowAny,IsAuthenticated
from rest_framework_simplejwt.authentication import JWTAuthentication
from rest_framework.response import Response
from rest_framework.decorators import action
from rest_framework import status
from rest_framework.viewsets import ReadOnlyModelViewSet


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
        print("Perform create in viewsets")
        current_user = self.request.user
        print(f"Current user in create viewset: {current_user}")
        serializer.context['current_user'] = current_user
        serializer.save()

    def perform_update(self, serializer):
        print("Perform update in viewsets")
        current_user = self.request.user
        print(f"Current user in viewset: {current_user}")
        serializer.context['current_user'] = current_user
        serializer.save()

    @action(detail=False, methods=['get'])
    def user_bookings(self, request):
        email = request.query_params.get('email', None)
        if email:
            bookings = TransferBooking.objects.filter(email=email).select_related('driver', 'transfer_name')
            serializer = self.get_serializer(bookings, many=True)
            return Response(serializer.data)
        return Response({'error': 'Email parameter is required'}, status=400)
    
    @action(detail=True, methods=['patch'])
    def update_booking_status(self, request, pk=None):
        if not request.user.is_authenticated:
            return Response({'error': 'Authentication required'}, status=status.HTTP_401_UNAUTHORIZED)
        
        if request.user.user_type != 'driver':
            return Response({'error': 'Only drivers can update booking status'}, 
                        status=status.HTTP_403_FORBIDDEN)
        
        try:
            booking = TransferBooking.objects.get(pk=pk, driver=request.user)
        except TransferBooking.DoesNotExist:
            return Response({'error': 'Booking not found'}, status=status.HTTP_404_NOT_FOUND)

        new_status = request.data.get('status')
        
        # Validate status transition
        valid_transitions = {
            'pending': ['ongoing'],
            'ongoing': ['done'],
        }
        
        if booking.status not in valid_transitions or new_status not in valid_transitions.get(booking.status, []):
            return Response({
                'error': f'Invalid status transition from {booking.status} to {new_status}'
            }, status=status.HTTP_400_BAD_REQUEST)
        
        booking.status = new_status
        booking.save()
        
        serializer = DriverTransferBookingSerializer(booking)
        return Response(serializer.data)
    

class TransferBookingAuditViewSet(ReadOnlyModelViewSet):
    queryset = TransferBookingAudit.objects.all()
    serializer_class = TransferBookingAuditSerializer
    
    def get_queryset(self):
        return TransferBookingAudit.objects.select_related(
            'user', 'transfer_booking'
        ).order_by('-timestamp')[:10] 
