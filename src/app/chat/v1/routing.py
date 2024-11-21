from django.urls import path

from app.chat.v1.consumers import ChatConsumer

websocket_urlpatterns = [
    path("ws/", ChatConsumer.as_asgi()),
]
