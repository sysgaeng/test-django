import base64
import hashlib
import hmac

import requests
from django.conf import settings
from django.db import models
from django.utils import timezone

from app.common.models import BaseModel


class AlarmTalkLogStatus(models.TextChoices):
    READY = "R", "대기"
    SUCCESS = "S", "성공"
    FAILURE = "F", "실패"


class AlarmTalkLog(BaseModel):
    to_set = models.JSONField(verbose_name="수신자", default=list)
    template_code = models.CharField(verbose_name="템플릿코드", max_length=32)
    title = models.CharField(verbose_name="제목", max_length=128)
    content = models.TextField(verbose_name="내용")
    status = models.CharField(
        verbose_name="상태", max_length=1, choices=AlarmTalkLogStatus.choices, default=AlarmTalkLogStatus.READY
    )
    fail_reason = models.TextField(verbose_name="실패사유", blank=True, default="")

    class Meta:
        db_table = "alarmtalk_log"
        verbose_name = "알람톡 로그"
        verbose_name_plural = verbose_name

    def send(self):
        sms_uri = f"/alimtalk/v2/services/{settings.ALARMTALK_ID}/messages"
        url = f"https://sens.apigw.ntruss.com{sms_uri}"
        timestamp = str(int(timezone.now().timestamp() * 1000))
        hash_str = f"POST {sms_uri}\n{timestamp}\n{settings.ALARMTALK_CLIENT_ID}"

        digest = hmac.new(
            bytes(settings.ALARMTALK_CLIENT_SECRET, "utf-8"), hash_str.encode("utf-8"), hashlib.sha256
        ).digest()
        d_hash = base64.b64encode(digest).decode()
        headers = {
            "Content-Type": "application/json; charset=utf-8",
            "x-ncp-apigw-timestamp": timestamp,
            "x-ncp-iam-access-key": settings.ALARMTALK_CLIENT_ID,
            "x-ncp-apigw-signature-v2": d_hash,
        }

        data = {
            "plusFriendId": settings.ALARMTALK_PLUS_ID,
            "templateCode": self.template_code,
            "messages": [
                {
                    "to": to,
                    "content": self.content,
                    "buttons": [
                        {
                            "type": "string",
                            "name": "string",
                            "linkMobile": "string",
                            "linkPc": "string",
                            "schemeIos": "string",
                            "schemeAndroid": "string",
                        }
                    ],
                    "useSmsFailover": True,
                }
                for to in self.to_set
            ],
        }
        response = requests.post(url, headers=headers, json=data)
        if response.ok:
            self.status = AlarmTalkLogStatus.SUCCESS
        else:
            self.status = AlarmTalkLogStatus.FAILURE
        self.save()
