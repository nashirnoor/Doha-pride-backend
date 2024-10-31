from rest_framework import generics
from .models import ToursAndActivities,TopActivities
from .serailizers import ToursAndActivitiesSerializer,TopActivitiesSerializer
from rest_framework.permissions import AllowAny

class ToursAndActivitiesDetailView(generics.RetrieveAPIView):
    permission_classes = [AllowAny]
    queryset = ToursAndActivities.objects.all()
    serializer_class = ToursAndActivitiesSerializer
    lookup_field = 'id'

    def retrieve(self, request, *args, **kwargs):
        print(f"Retrieving tour with id: {kwargs.get('id')}")
        return super().retrieve(request, *args, **kwargs)

class ToursListView(generics.ListCreateAPIView):
    permission_classes = [AllowAny]
    queryset = ToursAndActivities.objects.all()
    serializer_class = ToursAndActivitiesSerializer

class TopActivitiesListView(generics.ListCreateAPIView):
    permission_classes = [AllowAny]
    queryset = TopActivities.objects.all()
    serializer_class = TopActivitiesSerializer




# views.py
from rest_framework.response import Response
from rest_framework.views import APIView
from rest_framework import status
from django.core.mail import send_mail
from .serailizers import TourBookingSerializer
import logging

logger = logging.getLogger(__name__)

class TourBookingView(APIView):
    def post(self, request):
        serializer = TourBookingSerializer(data=request.data)
        
        if serializer.is_valid():
            name = serializer.validated_data['name']
            email = serializer.validated_data['email']
            date = serializer.validated_data['date']
            time = serializer.validated_data['time']
            phone = serializer.validated_data['phone']
            
            subject = 'Tour Booking Confirmation'
            message = f"User {name} has booked a tour.\n\nDetails:\nName: {name}\nEmail: {email}\nDate: {date}\nTime: {time}"
            recipient_list = ['nashirnoor2002@gmail.com']
            
            try:
                logger.info('Sending email...')
                send_mail(subject, message, 'your-email@gmail.com', recipient_list)
                logger.info('Email sent successfully!')
            except Exception as e:
                logger.error(f'Error sending email: {str(e)}', exc_info=True)
                return Response({'error': 'Failed to send email'}, status=status.HTTP_500_INTERNAL_SERVER_ERROR)
            
            return Response({'message': 'Booking successful and email sent!'}, status=status.HTTP_200_OK)
        
        return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)
