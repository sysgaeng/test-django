# required
# method: POST
# timezone: UTC
# cron expressions document
# https://docs.aws.amazon.com/eventbridge/latest/userguide/eb-cron-expressions.html
from django.urls import path

SCHEDULES = dict(
    # schedule_name={
    #     "path": path("cron/test/", TestCron.as_view()),
    #     "cron": "* * * * ? *",
    # },
)
