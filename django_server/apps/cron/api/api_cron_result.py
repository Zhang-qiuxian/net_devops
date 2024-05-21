from public.mixins import ReadOnlyModelViewSet

from django_celery_results.models import TaskResult
from apps.cron.models import CronJobSyncLog

from apps.cron.serial import TaskResultSerializer, CronJobSyncLogSerializer


class TaskResultViewSet(ReadOnlyModelViewSet):
    queryset = TaskResult.objects.all().order_by('-id')
    serializer_class = TaskResultSerializer


class CronJobSyncLogViewSet(ReadOnlyModelViewSet):
    queryset = CronJobSyncLog.objects.all().order_by('-id')
    serializer_class = CronJobSyncLogSerializer


task_result = TaskResultViewSet
cron_log_result = CronJobSyncLogViewSet
