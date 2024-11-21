import math

from django.db import models
from firebase_admin import messaging

from app.common.models import BaseModel


class PushLogStatus(models.TextChoices):
    READY = "R", "대기"
    SUCCESS = "S", "성공"
    FAILURE = "F", "실패"


class PushLog(BaseModel):
    to_set = models.ManyToManyField("device.Device", verbose_name="수신자")
    title = models.CharField(verbose_name="제목", max_length=128)
    content = models.TextField(verbose_name="내용")
    status = models.CharField(
        verbose_name="상태", max_length=1, choices=PushLogStatus.choices, default=PushLogStatus.READY
    )
    fail_reason = models.TextField(verbose_name="실패사유", blank=True, default="")

    class Meta:
        db_table = "push_log"
        verbose_name = "푸시 로그"
        verbose_name_plural = verbose_name

    def send(self):
        device_set = self.to_set.all()
        failed_device_set = []
        for i in range(math.ceil(len(device_set) / 500)):
            message = messaging.MulticastMessage(
                tokens=[device.token for device in device_set[500 * i : 500 * (i + 1)]],
                notification=messaging.Notification(
                    title=self.title,
                    body=self.content,
                ),
            )
            response = messaging.send_each_for_multicast(message)
            if response.failure_count > 0:
                responses = response.responses
                for idx, resp in enumerate(responses):
                    if not resp.success:
                        failed_device_set.append(device_set[idx])
        self.to_set.model.objects.filter(id__in=[device.id for device in failed_device_set]).delete()
