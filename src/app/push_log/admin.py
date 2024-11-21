from django.contrib import admin

from app.push_log.models import PushLog


@admin.register(PushLog)
class PushLogAdmin(admin.ModelAdmin):
    pass
