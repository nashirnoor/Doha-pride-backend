from rest_framework import serializers
from .models import HotelCategory,HotelSubcategory,TourBooking,TransferBooking,TransferBookingAudit,TourBookingAudit

class BookingSerializer(serializers.ModelSerializer):
    class Meta:
        model = TourBooking
        fields = ['id', 'name','tour_name', 'email', 'number', 'date','driver','time', 'status','tour_activity','hotel_name','vehicle','flight','room_no','amount','voucher_no','note','unique_code','travel_agency']
        read_only_fields = ['unique_code','travel_agency']

        def get_tour_service_name(self, obj):
          return obj.tour_activity if obj.tour_activity else None
        
        def create(self, validated_data):
            current_user = self.context.get('current_user')
            print(f"Current user in serializer create: {current_user}")
            # Create the instance without _current_user in validated_data
            instance = TourBooking.objects.create(**validated_data)
            # Set _current_user after creation
            instance._current_user = current_user
            instance.save()
        
            return instance

    def update(self, instance, validated_data):
        current_user = self.context.get('current_user')
        instance._current_user = current_user
        
        for attr, value in validated_data.items():
            setattr(instance, attr, value)
            
        instance.save()
        return instance
    

class TransferBookingSerializer(serializers.ModelSerializer):
    driver_name = serializers.SerializerMethodField()
    transfer_service_name = serializers.SerializerMethodField()

    class Meta:
        model = TransferBooking
        fields = [
            'id', 'name', 'email', 'number', 'date', 'time', 'status',
            'transfer_name', 'from_location', 'to_location', 'driver',
            'driver_name', 'transfer_service_name', 'hotel_name', 'vehicle',
            'flight', 'room_no', 'voucher_no', 'note', 'unique_code','amount',
            'travel_agency'
        ]
        read_only_fields = ['unique_code','travel_agency']

    def create(self, validated_data):
        current_user = self.context.get('current_user')
        print(f"Current user in serializer create: {current_user}")
        
        # Create the instance without _current_user in validated_data
        instance = TransferBooking.objects.create(**validated_data)
        
        # Set _current_user after creation
        instance._current_user = current_user
        instance.save()
        
        return instance

    def update(self, instance, validated_data):
        current_user = self.context.get('current_user')
        instance._current_user = current_user
        
        for attr, value in validated_data.items():
            setattr(instance, attr, value)
            
        instance.save()
        return instance
    
    def get_driver_name(self, obj):
        return obj.driver.username if obj.driver else None

    def get_transfer_service_name(self, obj):
        return obj.transfer_name.name if obj.transfer_name else None

    
class DriverTransferBookingSerializer(serializers.ModelSerializer):
    class Meta:
        model = TransferBooking
        fields = ['id', 'name', 'email', 'number', 'date', 'time', 'from_location', 'to_location', 'status']
        read_only_fields = ['id', 'name', 'email', 'number', 'date', 'time', 'from_location', 'to_location']



class TransferBookingAuditSerializer(serializers.ModelSerializer):
    staff_name = serializers.SerializerMethodField()
    booking_name = serializers.SerializerMethodField()
    
    class Meta:
        model = TransferBookingAudit
        fields = ['id', 'staff_name','user', 'action', 'field_name', 'old_value', 
                 'new_value', 'timestamp', 'booking_name']
    
    def get_staff_name(self, obj):
        return obj.user.username if obj.user else 'System'
    
    def get_booking_name(self, obj):
        return f"{obj.transfer_booking.name} ({obj.transfer_booking.unique_code})"
    

class TourBookingAuditSerializer(serializers.ModelSerializer):
    staff_name = serializers.SerializerMethodField()
    booking_name = serializers.SerializerMethodField()
    
    class Meta:
        model = TourBookingAudit
        fields = ['id', 'staff_name','user', 'action', 'field_name', 'old_value', 
                 'new_value', 'timestamp', 'booking_name']
    
    def get_staff_name(self, obj):
        return obj.user.username if obj.user else 'System'
    
    def get_booking_name(self, obj):
        return f"{obj.tour_booking.name} ({obj.tour_booking.unique_code})"
    






class SubcategorySerializer(serializers.ModelSerializer):
    class Meta:
        model = HotelSubcategory
        fields = ['id', 'name']

class HotelCategorySerializer(serializers.ModelSerializer):
    subcategories = SubcategorySerializer(many=True, read_only=True)

    class Meta:
        model = HotelCategory
        fields = ['id', 'hotel_name', 'subcategories']