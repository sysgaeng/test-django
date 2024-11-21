from drf_spectacular.utils import extend_schema, extend_schema_view
from rest_framework import mixins
from rest_framework.viewsets import GenericViewSet

from app.common.pagination import CursorPagination
from app.message.models import Message
from app.message.v1.filters import MessageFilter
from app.message.v1.permissions import MessagePermission
from app.message.v1.serializers import MessageSerializer


@extend_schema_view(
    list=extend_schema(summary="Message 목록 조회"),
    create=extend_schema(summary="Message 등록"),
)
class MessageViewSet(
    mixins.ListModelMixin,
    mixins.CreateModelMixin,
    GenericViewSet,
):
    queryset = Message.objects.all()
    serializer_class = MessageSerializer
    permission_classes = [MessagePermission]
    pagination_class = CursorPagination
    filter_class = MessageFilter

    def get_queryset(self):
        queryset = super().get_queryset()
        return queryset
