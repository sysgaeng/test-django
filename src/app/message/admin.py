from django.contrib import admin

from app.message.models import Message


@admin.register(Message)
class MessageAdmin(admin.ModelAdmin):
    pass
