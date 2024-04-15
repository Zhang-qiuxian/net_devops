from public.mixins import ModelViewSet

from django_celery_beat.models import ClockedSchedule, CrontabSchedule, IntervalSchedule, PeriodicTask, PeriodicTasks, \
    SolarSchedule
from apps.cron.serial import CrontabScheduleSerializer, IntervalScheduleSerializer, SolarScheduleSerializer, \
    PeriodicTasksSerializer, ClockedScheduleSerializer, PeriodicTaskSerializer


class ClockedScheduleAPI(ModelViewSet):
    queryset = ClockedSchedule.objects.all()
    serializer_class = ClockedScheduleSerializer


class IntervalScheduleAPI(ModelViewSet):
    queryset = IntervalSchedule.objects.all()
    serializer_class = IntervalScheduleSerializer


class CrontabScheduleAPI(ModelViewSet):
    queryset = CrontabSchedule.objects.all()
    serializer_class = CrontabScheduleSerializer


class PeriodicTaskAPI(ModelViewSet):
    queryset = PeriodicTask.objects.all()
    serializer_class = PeriodicTaskSerializer


class CronSolarSchedulesAPI(ModelViewSet):
    queryset = SolarSchedule.objects.all()
    serializer_class = SolarScheduleSerializer


class PeriodicTasksAPI(ModelViewSet):
    queryset = PeriodicTasks.objects.all()
    serializer_class = PeriodicTasksSerializer


clock_schedule = ClockedScheduleAPI
interval_schedule = IntervalScheduleAPI
periodic_task = PeriodicTaskAPI
cron_solar_schedules = CronSolarSchedulesAPI
periodic_tasks = PeriodicTasksAPI
