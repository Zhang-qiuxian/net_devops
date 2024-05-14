import base64, pickle
from typing import Any

from rest_framework.fields import SerializerMethodField
from rest_framework.serializers import ModelSerializer, CharField

from django_celery_beat.models import ClockedSchedule, CrontabSchedule, IntervalSchedule, PeriodicTask, PeriodicTasks, \
    SolarSchedule
from timezone_field import TimeZoneField

from django_celery_results.models import TaskResult, ChordCounter, GroupResult


class ClockedScheduleSerializer(ModelSerializer):
    class Meta:
        model = ClockedSchedule
        fields = '__all__'


class CrontabScheduleSerializer(ModelSerializer):
    timezone = CharField()

    class Meta:
        model = CrontabSchedule
        fields = '__all__'


class IntervalScheduleSerializer(ModelSerializer):
    class Meta:
        model = IntervalSchedule
        fields = '__all__'


class PeriodicTaskSerializer(ModelSerializer):
    class Meta:
        model = PeriodicTask
        fields = '__all__'


class PeriodicTasksSerializer(ModelSerializer):
    class Meta:
        model = PeriodicTasks
        fields = '__all__'


def handle_celery_result(result: str) -> Any:
    base: bytes = base64.b64decode(result)
    return pickle.loads(base)


class TaskResultSerializer(ModelSerializer):
    result = SerializerMethodField()
    meta = SerializerMethodField()

    def get_result(self, obj: TaskResult):
        return handle_celery_result(result=obj.result)

    def get_meta(self, obj: TaskResult):
        return handle_celery_result(result=obj.meta)

    class Meta:
        model = TaskResult
        fields = '__all__'

