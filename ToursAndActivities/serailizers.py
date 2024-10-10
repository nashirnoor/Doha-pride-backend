from rest_framework import serializers
from .models import ToursAndActivities, TourImage, TopActivities
from django.utils import timezone


class TourImageSerializer(serializers.ModelSerializer):
    class Meta:
        model = TourImage
        fields = ['id', 'image', 'alt_text']

class ToursAndActivitiesSerializer(serializers.ModelSerializer):
    media_gallery = TourImageSerializer(many=True, read_only=True)

    class Meta:
        model = ToursAndActivities
        fields = [
            'id', 'title', 'description', 'media_gallery', 
            'min_age', 'max_age', 'passengers_count', 'start_date', 'end_date','price'
        ]
    
    

class TopActivitiesSerializer(serializers.ModelSerializer):
    class Meta:
        model = TopActivities
        fields = ['id', 'name', 'description', 'image']



# serializers.py
from rest_framework import serializers

class TourBookingSerializer(serializers.Serializer):
    name = serializers.CharField(max_length=100)
    email = serializers.EmailField()
    date = serializers.DateField()
    time = serializers.TimeField()
    phone = serializers.CharField(max_length=15)
