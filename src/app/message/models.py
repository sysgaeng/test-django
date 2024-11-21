import json

import boto3
from boto3.dynamodb.conditions import Key
from botocore.exceptions import ClientError
from django.conf import settings
from django.db import models

from app.common.models import BaseModel


class Message(BaseModel):
    chat = models.ForeignKey("chat.Chat", verbose_name="채팅", on_delete=models.CASCADE)
    user = models.ForeignKey("user.User", verbose_name="유저", on_delete=models.CASCADE)
    text = models.TextField(verbose_name="텍스트", null=True, blank=True)
    image = models.URLField(verbose_name="이미지", null=True, blank=True)

    class Meta:
        db_table = "message"
        verbose_name = "메세지"
        verbose_name_plural = verbose_name
        ordering = ["-created_at"]

    def __str__(self):
        return self.text
