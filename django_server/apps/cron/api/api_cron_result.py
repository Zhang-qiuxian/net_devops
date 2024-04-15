from public.mixins import ModelViewSet

from django_celery_results.models import TaskResult, ChordCounter, GroupResult

from apps.cron.serial import TaskResultSerializer, ChordCounterSerializer, GroupResultSerializer


class TaskResultViewSet(ModelViewSet):
    queryset = TaskResult.objects.all()
    serializer_class = TaskResultSerializer


class ChordCounterViewSet(ModelViewSet):
    queryset = ChordCounter.objects.all()
    serializer_class = ChordCounterSerializer


class GroupResultViewSet(ModelViewSet):
    queryset = GroupResult.objects.all()
    serializer_class = GroupResultSerializer


task_result = TaskResultViewSet
chord_counter = ChordCounterViewSet
group_result = GroupResultViewSet
