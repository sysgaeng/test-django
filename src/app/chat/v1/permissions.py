from rest_framework.permissions import BasePermission

from app.chat.models import Chat


class IsChatOwner(BasePermission):
    def has_permission(self, request, view):
        pk = request.parser_context["kwargs"]["pk"]
        try:
            chat = Chat.objects.get(pk=pk)
            return request.user in chat.user_set.all()
        except Chat.DoesNotExist:
            return False
