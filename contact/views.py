from rest_framework.response import Response
from rest_framework.views import APIView
from rest_framework import status
from .models import Contact,ContactMessage
from .serializers import ContactSerializer,ContactMessageSerializer
from rest_framework.permissions import AllowAny
from rest_framework import generics


class ContactView(APIView):
    permission_classes = [AllowAny]
    def get(self, request):
        contact = Contact.objects.first()  # Assuming you have only one contact entry
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


class ContactMessageCreateView(generics.CreateAPIView):
    queryset = ContactMessage.objects.all()
    serializer_class = ContactMessageSerializer