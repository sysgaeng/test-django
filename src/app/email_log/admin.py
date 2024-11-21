from django.contrib import admin

from app.email_log.models import EmailLog


@admin.register(EmailLog)
class EmailLogAdmin(admin.ModelAdmin):
    pass
