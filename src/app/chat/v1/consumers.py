from channels.generic.websocket import AsyncJsonWebsocketConsumer
from djangorestframework_camel_case.util import camelize, underscoreize

from app.chat.models import Chat, Message


class ChatConsumer(AsyncJsonWebsocketConsumer):
    authentication = False

    async def connect(self):
        if self.authentication and not self.scope["user"].is_authenticated:
            return await self.close()

        await self.channel_layer.group_add(
            f"user_{self.scope['user'].pk}",
            self.channel_name,
        )
        return await self.accept()

    async def disconnect(self, close_code):
        await self.channel_layer.group_discard(
            f"user_{self.scope['user'].pk}",
            self.channel_name,
        )

    async def receive_json(self, content, **kwargs):
        data = underscoreize(content)
        message = await self.create_message(data)
        chat = await self.get_chat(message.chat_id)
        for user in chat.user_set.all():
            await self.channel_layer.group_send(
                str(user.pk),
                {
                    "type": "send_json",
                    "kind": "message",
                    "data": data,
                },
            )

    async def send_json(self, content, close=False):
        del content["type"]
        await super().send_json(dict(camelize(content)), close)

    async def get_chat(self, chat_id):
        try:
            return await self.scope["user"].chat_set.prefetch_related("user_set").aget(pk=chat_id)
        except Chat.DoesNotExist:
            return None

    async def create_message(self, data):
        message = await Message.objects.acreate(
            chat_id=data["chat_id"],
            user=self.scope["user"],
            text=data["text"],
        )
        # 푸시 전송
        return message
