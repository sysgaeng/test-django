from django.contrib import admin

from app.alarmtalk_log.models import AlarmTalkLog


@admin.register(AlarmTalkLog)
class AlarmTalkLogAdmin(admin.ModelAdmin):
    pass
