from rest_framework import serializers
from .models import BackgroundVideo, CardOne, CardTwo

class BackgroundVideoSerializer(serializers.ModelSerializer):
    class Meta:
        model = BackgroundVideo
        fields = ['id', 'video']

class CardOneSerializer(serializers.ModelSerializer):
    class Meta:
        model = CardOne
        fields = ['id', 'image1', 'title', 'description']

class CardTwoSerializer(serializers.ModelSerializer):
    class Meta:
        model = CardTwo
        fields = ['id', 'image2', 'title2', 'description']
