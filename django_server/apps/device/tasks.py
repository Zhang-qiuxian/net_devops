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
