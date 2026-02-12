from rest_framework import viewsets, filters
from rest_framework.permissions import IsAuthenticated
from .models import Conversation, Message
from .serializers import ConversationSerializer, MessageSerializer
from .permissions import IsParticipantOfConversation
from .pagination import MessagePagination
from .filters import MessageFilter
from django_filters.rest_framework import DjangoFilterBackend




class ConversationViewSet(viewsets.ModelViewSet):
    queryset = Conversation.objects.all()
    serializer_class = ConversationSerializer
    permission_classes = [IsAuthenticated, IsParticipant]  
    filter_backends = [filters.SearchFilter]
    search_fields = ['participants__email']

    def create(self, request, *args, **kwargs):
        conversation = Conversation.objects.create()
        conversation.participants.add(request.user)
        serializer = self.get_serializer(conversation)
        return Response(serializer.data, status=status.HTTP_201_CREATED)


class MessageViewSet(viewsets.ModelViewSet):
    queryset = Message.objects.all()
    serializer_class = MessageSerializer
    permission_classes = [IsAuthenticated, IsParticipantOfConversation]
    filter_backends = [DjangoFilterBackend, filters.OrderingFilter]
    filterset_class = MessageFilter
    pagination_class = MessagePagination
    ordering_fields = ['sent_at']
    ordering = ['-sent_at']  
    
    def create(self, request, *args, **kwargs):
        conversation_id = request.data.get('conversation_id')
        message_body = request.data.get('message_body')

        if not request.user.is_authenticated:
            return Response(
                {"detail": "Authentication credentials were not provided."},
                status=status.HTTP_403_FORBIDDEN
            )

        allowed = Message.objects.filter(
            conversation_id=conversation_id,
            conversation__participants=request.user
        ).exists() or Conversation.objects.filter(
            id=conversation_id,
            participants=request.user
        ).exists()

        if not allowed:
            return Response(
                {"detail": "You do not have permission to send messages here."},
                status=status.HTTP_403_FORBIDDEN
            )

        message = Message.objects.create(
            sender=request.user,
            conversation_id=conversation_id,
            message_body=message_body,
        )
        serializer = self.get_serializer(message)
        return Response(serializer.data, status=status.HTTP_201_CREATED)
