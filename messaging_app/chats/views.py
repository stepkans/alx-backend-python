from rest_framework import viewsets, permissions, status
from rest_framework.response import Response
from .models import Conversation, Message, User
from .serializers import ConversationSerializer, MessageSerializer
from django.shortcuts import get_object_or_404
import django_filters.rest_framework as filters


class ConversationViewSet(viewsets.ModelViewSet):
    queryset = Conversation.objects.all()
    serializer_class = ConversationSerializer
    permission_classes = [permissions.IsAuthenticated]
    filter_backends = [filters.DjangoFilterBackend]

    def get_queryset(self):
        return Conversation.objects.filter(participants=self.request.user)

    def perform_create(self, serializer):
        conversation = serializer.save()
        user_ids = self.request.data.get("participant_ids", [])
        users = User.objects.filter(user_id__in=user_ids)
        conversation.participants.set(users)
        conversation.save()
        return Response(serializer.data, status=status.HTTP_201_CREATED)


class MessageViewSet(viewsets.ModelViewSet):
    serializer_class = MessageSerializer
    permission_classes = [permissions.IsAuthenticated]
    filter_backends = [filters.DjangoFilterBackend]

    def get_queryset(self):
        conversation_id = self.kwargs.get("conversation_pk")
        return Message.objects.filter(
            conversation__conversation_id=conversation_id,
            conversation__participants=self.request.user
        )

    def perform_create(self, serializer):
        conversation_id = self.kwargs.get("conversation_pk")
        conversation = get_object_or_404(Conversation, conversation_id=conversation_id)
        serializer.save(sender=self.request.user, conversation=conversation)
        return Response(serializer.data, status=status.HTTP_201_CREATED)