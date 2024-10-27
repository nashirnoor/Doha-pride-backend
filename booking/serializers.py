from rest_framework import serializers
from .models import TourBooking,TransferBooking,TransferBookingAudit

class BookingSerializer(serializers.ModelSerializer):
    class Meta:
        model = TourBooking
        fields = ['id', 'name', 'email', 'number', 'date','driver','time', 'status','tour_activity','hotel_name','vehicle','flight','room_no','amount','voucher_no','note','unique_code']
        read_only_fields = ['status','unique_code']

        def get_tour_service_name(self, obj):
          return obj.tour_activity if obj.tour_activity else None

class TransferBookingSerializer(serializers.ModelSerializer):
    driver_name = serializers.SerializerMethodField()
    transfer_service_name = serializers.SerializerMethodField()

    class Meta:
        model = TransferBooking
        fields = [
            'id', 'name', 'email', 'number', 'date', 'time', 'status',
            'transfer_name', 'from_location', 'to_location', 'driver',
            'driver_name', 'transfer_service_name', 'hotel_name', 'vehicle',
            'flight', 'room_no', 'voucher_no', 'note', 'unique_code','amount'
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


class TransferBookingAuditSerializer(serializers.ModelSerializer):
    staff_name = serializers.SerializerMethodField()
    booking_name = serializers.SerializerMethodField()
    
    class Meta:
        model = TransferBookingAudit
        fields = ['id', 'staff_name', 'action', 'field_name', 'old_value', 
                 'new_value', 'timestamp', 'booking_name']
    
    def get_staff_name(self, obj):
        return obj.user.username if obj.user else 'System'
    
    def get_booking_name(self, obj):
        return f"{obj.transfer_booking.name} ({obj.transfer_booking.unique_code})"