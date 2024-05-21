from rest_framework.request import Request
from rest_framework.response import Response

from public.mixins import ModelViewSet

from django_celery_beat.models import ClockedSchedule, CrontabSchedule, IntervalSchedule, PeriodicTask
from apps.cron.serial import CrontabScheduleSerializer, IntervalScheduleSerializer, \
    ClockedScheduleSerializer, PeriodicTaskSerializer
from rest_framework.decorators import action

from public.response import ResponseOK


class ClockedScheduleAPI(ModelViewSet):
    queryset = ClockedSchedule.objects.all().order_by('id')
    serializer_class = ClockedScheduleSerializer


class IntervalScheduleAPI(ModelViewSet):
    queryset = IntervalSchedule.objects.all().order_by('id')
    serializer_class = IntervalScheduleSerializer


class CrontabScheduleAPI(ModelViewSet):
    queryset = CrontabSchedule.objects.all().order_by('id')
    serializer_class = CrontabScheduleSerializer


class PeriodicTaskAPI(ModelViewSet):
    queryset = PeriodicTask.objects.all().order_by('id')
    serializer_class = PeriodicTaskSerializer

    @action(methods=['get'], detail=False)
    def tasks(self, request: Request) -> Response:
        from celery import current_app
        _ = current_app.loader.import_default_modules()
        exclude_str: list[str] = ['celery', 'django_server']
        tasks = list(sorted(name for name in current_app.tasks if not name.split('.')[0] in exclude_str))
        return ResponseOK({'tasks': tasks})


clock_schedule = ClockedScheduleAPI
interval_schedule = IntervalScheduleAPI
periodic_task = PeriodicTaskAPI
crontab_schedules = CrontabScheduleAPI
