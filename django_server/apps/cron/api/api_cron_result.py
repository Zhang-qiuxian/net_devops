from public.mixins import ReadOnlyModelViewSet

from django_celery_results.models import TaskResult, ChordCounter, GroupResult

from apps.cron.serial import TaskResultSerializer


class TaskResultViewSet(ReadOnlyModelViewSet):
    queryset = TaskResult.objects.all().order_by('id')
    serializer_class = TaskResultSerializer


task_result = TaskResultViewSet

