from rest_framework import viewsets
from .models import TourBooking,TransferBooking,TransferBookingAudit,HotelCategory,TourBookingAudit
from .serializers import BookingSerializer,TransferBookingSerializer,TransferBookingAuditSerializer,DriverTransferBookingSerializer,HotelCategorySerializer,TourBookingAuditSerializer
from django.views.decorators.csrf import csrf_exempt
from django.utils.decorators import method_decorator
from rest_framework.permissions import AllowAny,IsAuthenticated
from rest_framework_simplejwt.authentication import JWTAuthentication
from rest_framework.response import Response
from rest_framework.decorators import action
from rest_framework.views import APIView
from rest_framework import status
from rest_framework.viewsets import ReadOnlyModelViewSet


class BookingViewSet(viewsets.ModelViewSet):
    permission_classes = [AllowAny]
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
    
    @csrf_exempt
    @action(detail=True, methods=['patch'], permission_classes=[IsAuthenticated])
    def update_booking_status(self, request, pk=None):
        print("INnnnnn")
        if not request.user.is_authenticated:
            return Response({'error': 'Authentication required'}, status=status.HTTP_401_UNAUTHORIZED)
        
        if request.user.user_type != 'driver':
            print("drivereer")
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
    
class TourBookingAuditViewSet(ReadOnlyModelViewSet):
    queryset = TourBookingAudit.objects.all()
    serializer_class = TourBookingAuditSerializer
    
    def get_queryset(self):
        return TourBookingAudit.objects.select_related(
            'user', 'tour_booking'
        ).order_by('-timestamp')[:10] 
    
    

class CategoryListView(APIView):
    permission_classes = [AllowAny]  

    def get(self, request):
        categories = HotelCategory.objects.prefetch_related('subcategories').all()
        serializer = HotelCategorySerializer(categories, many=True)
        return Response(serializer.data)
    

from rest_framework.permissions import BasePermission
from rest_framework.exceptions import PermissionDenied

class IsTravelAgencyUser(BasePermission):
    def has_permission(self, request, view):
        return request.user.is_authenticated and request.user.user_type == 'travel_agency'

@method_decorator(csrf_exempt, name='dispatch')
class TravelAgencyTransferBookingsViewSet(viewsets.ModelViewSet):
    authentication_classes = [JWTAuthentication]
    permission_classes = [IsTravelAgencyUser]
    serializer_class = TransferBookingSerializer

    def get_queryset(self):
        # Only return bookings created by the current travel agency
        return TransferBooking.objects.filter(travel_agency=self.request.user)

    def perform_create(self, serializer):
        serializer.context['current_user'] = self.request.user
        serializer.save(travel_agency=self.request.user)

    def perform_update(self, serializer):
        # Ensure the travel agency can only update their own bookings
        if serializer.instance.travel_agency != self.request.user:
            raise PermissionDenied("You can only update your own bookings")
        
        serializer.context['current_user'] = self.request.user
        serializer.save()

@method_decorator(csrf_exempt, name='dispatch')
class TravelAgencyTourBookingsViewSet(viewsets.ModelViewSet):
    authentication_classes = [JWTAuthentication]
    permission_classes = [IsTravelAgencyUser]
    serializer_class = BookingSerializer

    def get_queryset(self):
        # Only return bookings created by the current travel agency
        return TourBooking.objects.filter(travel_agency=self.request.user)

    def perform_create(self, serializer):
        serializer.context['current_user'] = self.request.user
        serializer.save(travel_agency=self.request.user)

    def perform_update(self, serializer):
        # Ensure the travel agency can only update their own bookings
        if serializer.instance.travel_agency != self.request.user:
            raise PermissionDenied("You can only update your own bookings")
        
        serializer.context['current_user'] = self.request.user
        serializer.save()





























from rest_framework.views import APIView
from rest_framework.response import Response
from rest_framework import status
from django.db.models import Count
from django.db.models.functions import ExtractMonth
from datetime import datetime
from django.contrib.auth import get_user_model

class DashboardStatsView(APIView):
    permission_classes = [AllowAny]
    def get(self, request):
        try:
            current_month = datetime.now().month
            current_year = datetime.now().year

            transfer_monthly = TransferBooking.objects.filter(
                status__in=['done', 'pending', 'posted'],
                date__year=current_year
            ).annotate(
                month=ExtractMonth('date')
            ).values('month').annotate(
                bookings=Count('id')
            ).order_by('month')

            tour_monthly = TourBooking.objects.filter(
                status__in=['done', 'pending', 'posted'],
                date__year=current_year
            ).annotate(
                month=ExtractMonth('date')
            ).values('month').annotate(
                bookings=Count('id')
            ).order_by('month')

            current_transfer_count = TransferBooking.objects.filter().count()

            current_tour_count = TourBooking.objects.filter(
                status__in=['done', 'pending', 'posted'],
                date__year=current_year,
                date__month=current_month
            ).count()

            # Get driver count
            driver_count = get_user_model().objects.filter(user_type='driver').count()

            # Get pending counts
            pending_transfers = TransferBooking.objects.filter(status='pending').count()
            pending_tours = TourBooking.objects.filter(status='pending').count()

            # Format monthly data
            months = ['Jan', 'Feb', 'Mar', 'Apr', 'May', 'Jun', 'Jul', 'Aug', 'Sep', 'Oct', 'Nov', 'Dec']
            
            transfer_data = [
                {
                    'month': months[item['month']-1],
                    'bookings': item['bookings']
                } for item in transfer_monthly
            ]

            tour_data = [
                {
                    'month': months[item['month']-1],
                    'bookings': item['bookings']
                } for item in tour_monthly
            ]

            response_data = {
                'stats': {
                    'transfer_bookings': current_transfer_count,
                    'tour_bookings': current_tour_count,
                    'drivers': driver_count,
                    'pending_transfers': pending_transfers,
                    'pending_tours': pending_tours,
                },
                'transfer_monthly': transfer_data,
                'tour_monthly': tour_data
            }

            return Response(response_data, status=status.HTTP_200_OK)

        except Exception as e:
            return Response(
                {'error': str(e)}, 
                status=status.HTTP_500_INTERNAL_SERVER_ERROR
            )