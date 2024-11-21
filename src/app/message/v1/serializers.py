from rest_framework import serializers

from app.message.models import Message
from app.message.v1.nested_serializers import UserSerializer


class MessageSerializer(serializers.ModelSerializer):
    user = UserSerializer(label="유저", read_only=True)

    class Meta:
        model = Message
        fields = [
            "id",
            "user",
            "text",
            "image",
        ]

    def validate(self, attrs):
        attrs["user_id"] = self.context["request"].user.id
        return attrs

    def create(self, validated_data):
        instance = super().create(validated_data)
        user_set = instance.chat.user_set.exclude(user_id=instance.user_id)
        for user in user_set:
            instance.send(user.id)
        return instance
