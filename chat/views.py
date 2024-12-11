# from rest_framework.views import APIView
# from rest_framework.response import Response
# from rest_framework.permissions import IsAuthenticated
# from rest_framework import status
# from .models import ChatMessage
# from .serializers import ChatMessageSerializer
# from django.db.models import Q

# class ChatAPIView(APIView):
#     permission_classes = [IsAuthenticated]

#     def get(self, request):
#         # Get chat partner's user ID from query params
#         partner_id = request.query_params.get('partner_id')
        
#         if not partner_id:
#             return Response(
#                 {"error": "Partner ID is required"}, 
#                 status=status.HTTP_400_BAD_REQUEST
#             )

#         # Fetch messages between current user and partner
#         messages = ChatMessage.objects.filter(
#             Q(sender=request.user, receiver_id=partner_id) | 
#             Q(sender_id=partner_id, receiver=request.user)
#         ).order_by('timestamp')

#         serializer = ChatMessageSerializer(messages, many=True)
#         return Response(serializer.data)

#     def post(self, request):
#         # Send a new message
#         data = request.data.copy()
#         data['sender'] = request.user.id
        
#         serializer = ChatMessageSerializer(data=data)
#         if serializer.is_valid():
#             serializer.save(sender=request.user)
#             return Response(serializer.data, status=status.HTTP_201_CREATED)
        
#         return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)

# class UnreadMessagesView(APIView):
#     permission_classes = [IsAuthenticated]

#     def get(self, request):
#         # Get unread messages count for each chat partner
#         partner_id = request.query_params.get('partner_id')
        
#         if partner_id:
#             unread_count = ChatMessage.objects.filter(
#                 receiver=request.user, 
#                 sender_id=partner_id, 
#                 is_read=False
#             ).count()
#         else:
#             # If no partner specified, get total unread messages
#             unread_count = ChatMessage.objects.filter(
#                 receiver=request.user, 
#                 is_read=False
#             ).count()
        
#         return Response({"unread_count": unread_count})