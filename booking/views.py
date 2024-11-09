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
from rest_framework.decorators import api_view, authentication_classes, permission_classes
from django.db.models import Count
from django.db.models.functions import ExtractMonth
from django.contrib.auth import get_user_model
from contact.models import ContactMessage
from datetime import datetime
from rest_framework.viewsets import ReadOnlyModelViewSet
from rest_framework.pagination import PageNumberPagination
from django.db.models import Q
from django.utils import timezone
from django.db.models import F


@method_decorator(csrf_exempt, name='dispatch')
class BookingViewSet(viewsets.ModelViewSet):
    permission_classes = [AllowAny]
    queryset = TourBooking.objects.all()
    serializer_class = BookingSerializer

    def get_queryset(self):
        today = timezone.now().date()
        
        # First, sort by date
        queryset = TourBooking.objects.annotate(
            date_diff=F('date') - today
        ).order_by(
            # Put future dates first, sorted by closest to today
            F('date_diff').asc(nulls_last=True),
            # For same dates, sort by time
            'time'
        )
        
        return queryset

    def perform_create(self, serializer):
        print("Perform create in viewsets")
        current_user = None
        if self.request.user.is_authenticated:
            current_user = self.request.user
        print(f"Current user in create viewset: {current_user}")
        serializer.context['current_user'] = current_user
        serializer.save()

    def perform_update(self, serializer):
        print("Perform update in viewsets")
        current_user = self.request.user
        print(f"Current user in update viewset: {current_user}")
        serializer.context['current_user'] = current_user
        serializer.save()

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
        current_user = self.request.user if self.request.user.is_authenticated else None
        print(f"Current user in create viewset: {current_user}")
        serializer.context['current_user'] = current_user  # Set in context instead
        serializer.save()

    def perform_update(self, serializer):
        print("Perform update in viewsets")
        current_user = self.request.user
        print(f"Current user in update viewset: {current_user}")
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
    



class StandardResultsSetPagination(PageNumberPagination):
    page_size = 15
    page_size_query_param = 'page_size'
    max_page_size = 100

# views.py
from rest_framework.viewsets import ReadOnlyModelViewSet
from rest_framework.pagination import PageNumberPagination
from django.db.models import Q
import re

class StandardResultsSetPagination(PageNumberPagination):
    page_size = 15
    page_size_query_param = 'page_size'
    max_page_size = 100

class TransferBookingAuditViewSet(ReadOnlyModelViewSet):
    queryset = TransferBookingAudit.objects.all()
    serializer_class = TransferBookingAuditSerializer
    pagination_class = StandardResultsSetPagination
    
    def get_queryset(self):
        queryset = TransferBookingAudit.objects.select_related(
            'user', 'transfer_booking'
        ).order_by('-timestamp')
        
        search = self.request.query_params.get('search', '')
        booking_id = self.request.query_params.get('booking_id', '')
        
        if search:
            queryset = queryset.filter(
                Q(user__username__icontains=search) |
                Q(transfer_booking__name__icontains=search)
            )
            
        if booking_id:
            queryset = queryset.filter(
                transfer_booking__unique_code=booking_id
            )
            
        return queryset
    
class TourBookingAuditViewSet(ReadOnlyModelViewSet):
    queryset = TourBookingAudit.objects.all()
    serializer_class = TourBookingAuditSerializer
    pagination_class = StandardResultsSetPagination
    
    def get_queryset(self):
        queryset = TourBookingAudit.objects.select_related(
            'user', 'tour_booking'
        ).order_by('-timestamp')
        
        search = self.request.query_params.get('search', '')
        booking_id = self.request.query_params.get('booking_id', '')
        
        if search:
            queryset = queryset.filter(
                Q(user__username__icontains=search) |
                Q(tour_booking__name__icontains=search)
            )
            
        if booking_id:
            queryset = queryset.filter(
                tour_booking__unique_code=booking_id
            )
            
        return queryset


#Dashboard Stats in Admin side of Recent Actions
class TransferBookingAuditViewSetDashboard(ReadOnlyModelViewSet):
    queryset = TransferBookingAudit.objects.all()
    serializer_class = TransferBookingAuditSerializer
    
    def get_queryset(self):
        return TransferBookingAudit.objects.select_related(
            'user', 'transfer_booking'
        ).order_by('-timestamp')[:10] 


class TourBookingAuditViewSetDashboard(ReadOnlyModelViewSet):
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


@api_view(['GET'])
@authentication_classes([JWTAuthentication])
@permission_classes([IsTravelAgencyUser])
def get_agency_dashboard_stats(request):
    try:
        current_month = datetime.now().month
        current_year = datetime.now().year

        # Get transfer bookings statistics with monthly data
        transfer_bookings = TransferBooking.objects.filter(travel_agency=request.user)
        transfer_monthly = transfer_bookings.filter(
            status__in=['done', 'pending', 'posted'],
            date__year=current_year
        ).annotate(
            month=ExtractMonth('date')
        ).values('month').annotate(
            bookings=Count('id')
        ).order_by('month')

        # Get tour bookings statistics with monthly data
        tour_bookings = TourBooking.objects.filter(travel_agency=request.user)
        tour_monthly = tour_bookings.filter(
            status__in=['done', 'pending', 'posted'],
            date__year=current_year
        ).annotate(
            month=ExtractMonth('date')
        ).values('month').annotate(
            bookings=Count('id')
        ).order_by('month')

        # Get total counts
        transfer_bookings_count = transfer_bookings.count()
        tour_bookings_count = tour_bookings.count()

        # Get pending counts
        pending_transfer_bookings = transfer_bookings.filter(status='pending').count()
        pending_tour_bookings = tour_bookings.filter(status='pending').count()

        # Get driver count
        driver_count = get_user_model().objects.filter(user_type='driver').count()

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

        return Response({
            'stats': {
                'transfer_bookings': transfer_bookings_count,
                'pending_transfers': pending_transfer_bookings,
                'tour_bookings': tour_bookings_count,
                'pending_tours': pending_tour_bookings,
                'drivers': driver_count,
            },
            'transfer_data': transfer_data,
            'tour_data': tour_data,
        })

    except Exception as e:
        return Response(
            {'error': str(e)}, 
            status=status.HTTP_500_INTERNAL_SERVER_ERROR
        )


#Admin Dashboard
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
            pending_contact = ContactMessage.objects.filter(status='pending').count()

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
                    'pending_contact':pending_contact,
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