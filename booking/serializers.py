from rest_framework import serializers
from .models import TourBooking,TransferBooking

class BookingSerializer(serializers.ModelSerializer):
    class Meta:
        model = TourBooking
        fields = ['id', 'name', 'email', 'number', 'date', 'time', 'status','tour_activity']
        read_only_fields = ['status']


class TransferBookingSerializer(serializers.ModelSerializer):
    class Meta:
        model = TransferBooking
        fields = ['id', 'name', 'email', 'number', 'date', 'time', 'status','transfer_name', 'from_location', 'to_location','driver']
        read_only_fields = ['status']


class DriverTransferBookingSerializer(serializers.ModelSerializer):
    class Meta:
        model = TransferBooking
        fields = ['id', 'name', 'email', 'number', 'date', 'time', 'from_location', 'to_location', 'status']