import requests
from django.conf import settings
from django.db import models

from app.common.models import BaseModel


class EmailLogStatus(models.TextChoices):
    READY = "R", "대기"
    SUCCESS = "S", "성공"
    FAILURE = "F", "실패"


class EmailLog(BaseModel):
    to_set = models.JSONField(verbose_name="수신자", default=list)
    title = models.CharField(verbose_name="제목", max_length=128)
    content = models.TextField(verbose_name="내용")
    status = models.CharField(
        verbose_name="상태", max_length=1, choices=EmailLogStatus.choices, default=EmailLogStatus.READY
    )
    fail_reason = models.TextField(verbose_name="실패사유", blank=True, default="")

    class Meta:
        db_table = "email_log"
        verbose_name = "이메일 로그"
        verbose_name_plural = verbose_name

    def send(self):
        url = f"https://api.mailgun.net/v3/{settings.MAILGUN_DOMAIN}/messages"
        data = {
            "from": settings.MAILGUN_FROM_EMAIL,
            "to": self.to_set,
            "subject": self.title,
            "html": self.content,
        }
        response = requests.post(url=url, data=data, auth=("api", settings.MAILGUN_API_KEY))
        if response.ok:
            self.status = EmailLogStatus.SUCCESS
        else:
            self.status = EmailLogStatus.FAILURE
        self.save()
