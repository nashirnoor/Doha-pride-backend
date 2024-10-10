from rest_framework import serializers
from .models import Booking,TransferBooking

class BookingSerializer(serializers.ModelSerializer):
    class Meta:
        model = Booking
        fields = ['id', 'name', 'email', 'number', 'date', 'time', 'status','tour_activity']
        read_only_fields = ['status']


class TransferBookingSerializer(serializers.ModelSerializer):
    class Meta:
        model = TransferBooking
        fields = ['id', 'name', 'email', 'number', 'date', 'time', 'status','transfer_name']
        read_only_fields = ['status']