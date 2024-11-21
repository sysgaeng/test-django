from django.urls import include, path
from rest_framework.routers import DefaultRouter

from app.chat.v1.views import ChatViewSet

router = DefaultRouter()
router.register("chat", ChatViewSet, basename="chat")

urlpatterns = [
    path("", include(router.urls)),
]
