from rest_framework import serializers
from .models import Contact,ContactMessage

class ContactSerializer(serializers.ModelSerializer):
    class Meta:
        model = Contact
        fields = ['email', 'phone_number', 'location']


class ContactMessageSerializer(serializers.ModelSerializer):
    class Meta:
        model = ContactMessage
        fields = ['id', 'name', 'email', 'phone', 'message', 'created_at','status']
