from django.contrib import admin

from app.sms_log.models import SmsLog


@admin.register(SmsLog)
class SmsLogAdmin(admin.ModelAdmin):
    pass
