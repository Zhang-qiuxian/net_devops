from rest_framework.serializers import ModelSerializer,CharField

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


class SolarScheduleSerializer(ModelSerializer):
    class Meta:
        model = SolarSchedule
        fields = '__all__'


class TaskResultSerializer(ModelSerializer):
    class Meta:
        model = TaskResult
        fields = '__all__'


class ChordCounterSerializer(ModelSerializer):
    class Meta:
        model = ChordCounter
        fields = '__all__'


class GroupResultSerializer(ModelSerializer):
    class Meta:
        model = GroupResult
        fields = '__all__'
