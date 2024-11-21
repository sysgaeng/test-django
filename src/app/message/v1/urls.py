from django.urls import include, path
from rest_framework.routers import DefaultRouter

from app.message.v1.views import MessageViewSet

router = DefaultRouter()
router.register("message", MessageViewSet, basename="message")

urlpatterns = [
    path("", include(router.urls)),
]
