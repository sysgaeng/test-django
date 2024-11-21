from drf_spectacular.utils import extend_schema, extend_schema_view
from rest_framework import mixins
from rest_framework.permissions import IsAuthenticated
from rest_framework.viewsets import GenericViewSet

from app.chat.models import Chat
from app.chat.v1.paginations import ChatPagination
from app.chat.v1.serializers import ChatSerializer


@extend_schema_view(
    list=extend_schema(summary="채팅 목록 조회"),
    create=extend_schema(summary="채팅 생성"),
)
class ChatViewSet(
    mixins.ListModelMixin,
    mixins.CreateModelMixin,
    GenericViewSet,
):
    queryset = Chat.objects.prefetch_related("user_set").all()
    serializer_class = ChatSerializer
    pagination_class = ChatPagination
    permission_classes = [IsAuthenticated]

    def get_queryset(self):
        queryset = super().get_queryset()
        queryset = queryset.filter(user_set=self.request.user)
        return queryset
