from app.common.pagination import CursorPagination


class ChatPagination(CursorPagination):
    page_size = 20
    ordering = "-created_at"
