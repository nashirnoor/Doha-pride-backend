from rest_framework import serializers
from .models import TourBooking,TransferBooking

class BookingSerializer(serializers.ModelSerializer):
    class Meta:
        model = TourBooking
        fields = ['id', 'name', 'email', 'number', 'date', 'time', 'status','tour_activity']
        read_only_fields = ['status']

class TransferBookingSerializer(serializers.ModelSerializer):
    driver_name = serializers.SerializerMethodField()
    transfer_service_name = serializers.SerializerMethodField()

    class Meta:
        model = TransferBooking
        fields = [
            'id', 'name', 'email', 'number', 'date', 'time', 'status',
            'transfer_name', 'from_location', 'to_location', 'driver',
            'driver_name', 'transfer_service_name', 'hotel_name', 'vehicle',
            'flight', 'room_no', 'voucher_no', 'note', 'unique_code'
        ]
        read_only_fields = ['status', 'unique_code']

    def get_driver_name(self, obj):
        return obj.driver.username if obj.driver else None

    def get_transfer_service_name(self, obj):
        return obj.transfer_name.name if obj.transfer_name else None

    
class DriverTransferBookingSerializer(serializers.ModelSerializer):
    class Meta:
        model = TransferBooking
        fields = ['id', 'name', 'email', 'number', 'date', 'time', 'from_location', 'to_location', 'status']