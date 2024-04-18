import time

from celery import shared_task
from celery.app.task import Task


@shared_task
def add(x, y) -> Task:
    print("task----------111111----------")
    time.sleep(5)
    return x + y


@shared_task
def mul(x, y):
    print("task----------22222----------")
    return x * y


@shared_task
def start_sync(*args, **kwargs) -> Task:
    d: dict | list | None = kwargs.get('device', None)
    if d is None:
        return "同步完成！"

    return None
