import json
import time

from celery.signals import task_failure, task_prerun, task_success

from app.celery_log.models import CeleryLog, CeleryLogStatusChoices


@task_prerun.connect
def task_celery_prerun(sender=None, **kwargs):
    if not sender:
        return

    CeleryLog.objects.create(
        task_id=kwargs["task_id"],
        name=sender.name.split(".")[-1],
        status=CeleryLogStatusChoices.PENDING,
        args=json.dumps(kwargs.get("args", [])),
        kwargs=json.dumps(kwargs.get("kwargs", {})),
    )


@task_success.connect
def task_celery_success(sender=None, **kwargs):
    if not sender:
        return

    CeleryLog.objects.filter(task_id=sender.request.id).update(
        status=CeleryLogStatusChoices.SUCCESS,
    )


@task_failure.connect
def task_celery_failure(sender=None, **kwargs):
    if not sender:
        return

    CeleryLog.objects.filter(task_id=kwargs["task_id"]).update(
        status=CeleryLogStatusChoices.FAILURE,
        message=kwargs.get("einfo").exception,
    )
