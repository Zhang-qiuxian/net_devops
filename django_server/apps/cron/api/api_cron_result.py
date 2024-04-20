from public.mixins import ReadOnlyModelViewSet

from django_celery_results.models import TaskResult, ChordCounter, GroupResult

from apps.cron.serial import TaskResultSerializer, ChordCounterSerializer, GroupResultSerializer


class TaskResultViewSet(ReadOnlyModelViewSet):
    queryset = TaskResult.objects.all().order_by('id')
    serializer_class = TaskResultSerializer


class ChordCounterViewSet(ReadOnlyModelViewSet):
    queryset = ChordCounter.objects.all().order_by('id')
    serializer_class = ChordCounterSerializer


class GroupResultViewSet(ReadOnlyModelViewSet):
    queryset = GroupResult.objects.all().order_by('id')
    serializer_class = GroupResultSerializer


task_result = TaskResultViewSet
chord_counter = ChordCounterViewSet
group_result = GroupResultViewSet
