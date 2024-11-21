from rest_framework import serializers

from app.chat.models import Chat


class ChatSerializer(serializers.ModelSerializer):
    class Meta:
        model = Chat
        fields = ["id", "created_at"]
