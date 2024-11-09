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


from rest_framework import viewsets
from rest_framework.permissions import AllowAny
from .models import ContactMessage
from .serializers import ContactMessageSerializer

class ContactMessageViewSet(viewsets.ModelViewSet):
    queryset = ContactMessage.objects.all().order_by('-created_at')
    serializer_class = ContactMessageSerializer
    permission_classes = [AllowAny]

    def get_queryset(self):
        return ContactMessage.objects.all().order_by('-created_at')
    
    @csrf_exempt
    def dispatch(self, *args, **kwargs):
        return super().dispatch(*args, **kwargs)

    # def get_permissions(self):
    #     if self.action == 'create':
    #         return [AllowAny()]
    #     return super().get_permissions()
