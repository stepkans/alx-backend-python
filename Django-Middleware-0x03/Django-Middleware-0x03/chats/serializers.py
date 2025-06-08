from rest_framework import serializers
from .models import User, Conversation, Message
from django.utils.timesince import timesince


class UserSerializer(serializers.ModelSerializer):
    username = serializers.CharField()  # ✅ Explicit use of CharField

    class Meta:
        model = User
        fields = [
            "user_id",
            "username",
            "email",
            "first_name",
            "last_name",
            "phone_number",
        ]


class MessageSerializer(serializers.ModelSerializer):
    sender = UserSerializer(read_only=True)
    time_since_sent = (
        serializers.SerializerMethodField()
    )  # ✅ Use of SerializerMethodField

    class Meta:
        model = Message
        fields = [
            "message_id",
            "sender",
            "message_body",
            "sent_at",
            "time_since_sent",
        ]

    def get_time_since_sent(self, obj):
        return timesince(obj.sent_at) + " ago"


class ConversationSerializer(serializers.ModelSerializer):
    participants = UserSerializer(many=True, read_only=True)
    messages = MessageSerializer(many=True, read_only=True, source="messages")
    title = serializers.CharField(required=True)

    class Meta:
        model = Conversation
        fields = [
            "conversation_id",
            "title",
            "participants",
            "created_at",
            "messages",
        ]

    def validate_title(self, value):
        if len(value.strip()) < 3:
            raise serializers.ValidationError(
                "Conversation title must be at least 3 characters long."
            )  # ✅ Use of ValidationError
        return value