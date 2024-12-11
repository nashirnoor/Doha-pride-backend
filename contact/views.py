from rest_framework.response import Response
from rest_framework.views import APIView
from rest_framework import status
from .models import Contact,ContactMessage
from .serializers import ContactSerializer,ContactMessageSerializer
from rest_framework.permissions import AllowAny
from rest_framework import generics
from django.views.decorators.csrf import csrf_exempt
from django.utils.decorators import method_decorator



@method_decorator(csrf_exempt, name='dispatch')
class ContactView(APIView):
    permission_classes = [AllowAny]
    def get(self, request):
        contact = Contact.objects.first()  
        if contact:
            serializer = ContactSerializer(contact)
            return Response(serializer.data)
        return Response({"message": "Contact details not found"}, status=status.HTTP_404_NOT_FOUND)
    
    def put(self, request):
        contact = Contact.objects.first()
        serializer = ContactSerializer(contact, data=request.data)
        if serializer.is_valid():
            serializer.save()
            return Response(serializer.data)
        return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)

from rest_framework.views import APIView
from rest_framework.response import Response
from rest_framework import status
from rest_framework.permissions import AllowAny
from django.views.decorators.csrf import csrf_exempt
from django.utils.decorators import method_decorator

@method_decorator(csrf_exempt, name='dispatch')
class ContactMessageView(APIView):
    permission_classes = [AllowAny]
    
    def post(self, request):
        serializer = ContactMessageSerializer(data=request.data)
        if serializer.is_valid():
            serializer.save()
            return Response(serializer.data, status=status.HTTP_201_CREATED)
        return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)
    
    def get(self, request):
        contact_messages = ContactMessage.objects.all().order_by('-created_at')        
        serializer = ContactMessageSerializer(contact_messages, many=True)        
        return Response(serializer.data, status=status.HTTP_200_OK)
    
    def patch(self, request, pk):
        try:
            contact_message = ContactMessage.objects.get(pk=pk)
        except ContactMessage.DoesNotExist:
            return Response({"error": "Contact message not found"}, status=status.HTTP_404_NOT_FOUND)
        
        serializer = ContactMessageSerializer(contact_message, data=request.data, partial=True)
        if serializer.is_valid():
            serializer.save()
            return Response(serializer.data, status=status.HTTP_200_OK)
        return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)