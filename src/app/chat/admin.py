from django.contrib import admin

from app.chat.models import Chat


@admin.register(Chat)
class ChatAdmin(admin.ModelAdmin):
    pass
