from django.db import models

from app.common.models import BaseModel


class Chat(BaseModel):
    user_set = models.ManyToManyField("user.User", verbose_name="참여자", blank=True)
    password = None

    class Meta:
        db_table = "chat"
        verbose_name = "채팅"
        verbose_name_plural = verbose_name
        ordering = ["-updated_at", "-created_at"]

    def get_last_message(self):
        return self.message_set.first()
