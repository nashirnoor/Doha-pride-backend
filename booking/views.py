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
from django.db.models import F, Value, Case, When, IntegerField



@method_decorator(csrf_exempt, name='dispatch')
class BookingViewSet(viewsets.ModelViewSet):
    permission_classes = [AllowAny]
    queryset = TourBooking.objects.all()
    serializer_class = BookingSerializer

    def get_queryset(self):
        today = timezone.now().date()
        current_time = timezone.now().time()
        
        queryset = TourBooking.objects.annotate(
            # Calculate the difference in days
            date_diff=F('date') - today,
            # Priority for pending status
            status_priority=Case(
                When(status='pending', then=Value(0)),
                default=Value(1),
                output_field=IntegerField(),
            ),
            # Priority for today's bookings
            is_today=Case(
                When(date=today, then=Value(0)),
                default=Value(1),
                output_field=IntegerField(),
            )
        ).order_by(
            # First sort by status (pending first)
            'status_priority',
            # Then sort by whether it's today
            'is_today',
            # Then sort by date
            'date',
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
        

from rest_framework.views import APIView
from rest_framework.response import Response
from rest_framework import status
from django.db.models import Sum, Count
from django.utils import timezone
from datetime import datetime, timedelta
from django.db.models.functions import TruncMonth

class BookingCurrencyStatsView(APIView):
    permission_classes = [AllowAny]
    
    def get(self, request):
        selected_year = request.query_params.get('year', datetime.now().year)
        
        # Get monthly totals for both booking types
        tour_monthly = self.get_monthly_totals(TourBooking, selected_year)
        transfer_monthly = self.get_monthly_totals(TransferBooking, selected_year)
        
        # Get yearly totals for both booking types
        tour_yearly = self.get_yearly_totals(TourBooking, selected_year)
        transfer_yearly = self.get_yearly_totals(TransferBooking, selected_year)
        
        # Format the data for frontend
        formatted_data = {
            'monthly_data': self.combine_monthly_data(tour_monthly, transfer_monthly),
            'yearly_totals': self.combine_yearly_totals(tour_yearly, transfer_yearly),
            'available_years': self.get_available_years(),
            'booking_types': {
                'tour': {
                    'monthly': self.process_monthly_data(tour_monthly),
                    'yearly': self.process_yearly_totals(tour_yearly)
                },
                'transfer': {
                    'monthly': self.process_monthly_data(transfer_monthly),
                    'yearly': self.process_yearly_totals(transfer_yearly)
                }
            }
        }
        
        return Response(formatted_data)

    def get_monthly_totals(self, model, year):
        return (
            model.objects
            .filter(
                status='done',
                date__year=year
            )
            .annotate(month=TruncMonth('date'))
            .values('month', 'currency')
            .annotate(total=Sum('amount'))
            .order_by('month', 'currency')
        )

    def get_yearly_totals(self, model, year):
        return (
            model.objects
            .filter(
                status='done',
                date__year=year
            )
            .values('currency')
            .annotate(total=Sum('amount'))
        )

    def process_monthly_data(self, monthly_totals):
        month_dict = {}
        for entry in monthly_totals:
            month = entry['month'].strftime('%B')
            if month not in month_dict:
                month_dict[month] = {
                    'month': month,
                    'QAR': 0,
                    'GBP': 0,
                    'USD': 0,
                    'EUR': 0
                }
            month_dict[month][entry['currency']] = float(entry['total'] or 0)
        return list(month_dict.values())

    def process_yearly_totals(self, yearly_totals):
        totals = {
            'QAR': 0,
            'GBP': 0,
            'USD': 0,
            'EUR': 0
        }
        for entry in yearly_totals:
            totals[entry['currency']] = float(entry['total'] or 0)
        return totals

    def combine_monthly_data(self, tour_monthly, transfer_monthly):
        combined_dict = {}
        
        # Process both sets of monthly data
        for entry in list(tour_monthly) + list(transfer_monthly):
            month = entry['month'].strftime('%B')
            if month not in combined_dict:
                combined_dict[month] = {
                    'month': month,
                    'QAR': 0,
                    'GBP': 0,
                    'USD': 0,
                    'EUR': 0,
                    'QAR_tour': 0,
                    'GBP_tour': 0,
                    'USD_tour': 0,
                    'EUR_tour': 0,
                    'QAR_transfer': 0,
                    'GBP_transfer': 0,
                    'USD_transfer': 0,
                    'EUR_transfer': 0
                }
            
            # Add to combined total
            amount = float(entry['total'] or 0)
            currency = entry['currency']
            combined_dict[month][currency] += amount
            
            # Add to specific booking type total
            is_tour = entry in tour_monthly
            type_suffix = '_tour' if is_tour else '_transfer'
            combined_dict[month][currency + type_suffix] = amount

        return list(combined_dict.values())

    def combine_yearly_totals(self, tour_yearly, transfer_yearly):
        combined = {
            'total': {
                'QAR': 0,
                'GBP': 0,
                'USD': 0,
                'EUR': 0
            },
            'tour': {
                'QAR': 0,
                'GBP': 0,
                'USD': 0,
                'EUR': 0
            },
            'transfer': {
                'QAR': 0,
                'GBP': 0,
                'USD': 0,
                'EUR': 0
            }
        }
        
        # Process tour totals
        for entry in tour_yearly:
            currency = entry['currency']
            amount = float(entry['total'] or 0)
            combined['total'][currency] += amount
            combined['tour'][currency] = amount
            
        # Process transfer totals
        for entry in transfer_yearly:
            currency = entry['currency']
            amount = float(entry['total'] or 0)
            combined['total'][currency] += amount
            combined['transfer'][currency] = amount
            
        return combined

    def get_available_years(self):
        # Get years from both booking types
        tour_years = set(
            TourBooking.objects
            .filter(status='done')
            .dates('date', 'year')
            .values_list('date__year', flat=True)
        )
        
        transfer_years = set(
            TransferBooking.objects
            .filter(status='done')
            .dates('date', 'year')
            .values_list('date__year', flat=True)
        )
        
        # Combine and sort years
        all_years = sorted(tour_years.union(transfer_years), reverse=True)
        return list(all_years)