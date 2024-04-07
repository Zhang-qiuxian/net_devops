from rest_framework.viewsets import GenericViewSet
from rest_framework.response import Response
from rest_framework.settings import api_settings
from rest_framework.request import Request
from rest_framework.serializers import Serializer
from django.db.models.query import QuerySet
from public.response import Ok, Error


class CreateModelMixin:
    """
    Create a model instance.
    """

    def create(self, request: Request, *args, **kwargs) -> Response:
        serializer: Serializer = self.get_serializer(data=request.data)
        if not serializer.is_valid():
            return Error(message="校验失败!", data=serializer.errors)
        self.perform_create(serializer)

        return Ok(message="创建成功!", data=serializer.data)

    def perform_create(self, serializer: Serializer):
        serializer.save()



class ListModelMixin:
    """
    List a queryset.
    """

    def list(self, request: Request, *args, **kwargs) -> Response:
        queryset: QuerySet = self.filter_queryset(self.get_queryset())
        page = self.paginate_queryset(queryset)
        if page is not None:
            serializer = self.get_serializer(page, many=True)
            return self.get_paginated_response(serializer.data)

        serializer = self.get_serializer(queryset, many=True)
        return Ok(message="查询成功！", data=serializer.data)


class RetrieveModelMixin:
    """
    Retrieve a model instance.
    """

    def retrieve(self, request: Request, *args, **kwargs) -> Response:
        instance = self.get_object()
        serializer = self.get_serializer(instance)
        return Ok(message="查询成功！", data=serializer.data)


class UpdateModelMixin:
    """
    Update a model instance.
    """

    def update(self, request: Request, *args, **kwargs) -> Response:
        partial = kwargs.pop('partial', False)
        instance = self.get_object()
        serializer: Serializer = self.get_serializer(instance, data=request.data, partial=partial)
        if not serializer.is_valid():
            return Error(message="更新失败!", data=serializer.errors, )

        self.perform_update(serializer)

        if getattr(instance, '_prefetched_objects_cache', None):
            # If 'prefetch_related' has been applied to a queryset, we need to
            # forcibly invalidate the prefetch cache on the instance.
            instance._prefetched_objects_cache = {}

        return Ok(message="更新成功!", data=serializer.data)

    def perform_update(self, serializer: Serializer):
        serializer.save()

    def partial_update(self, request: Request, *args, **kwargs) -> Response:
        kwargs['partial'] = True
        return self.update(request, *args, **kwargs)


class DestroyModelMixin:
    """
    Destroy a model instance.
    """

    def destroy(self, request: Request, *args, **kwargs) -> Response:
        instance = self.get_object()
        self.perform_destroy(instance)
        return Ok()

    def perform_destroy(self, instance: QuerySet):
        instance.delete()


class ModelViewSet(CreateModelMixin,
                   RetrieveModelMixin,
                   UpdateModelMixin,
                   DestroyModelMixin,
                   ListModelMixin,
                   GenericViewSet):
    pass


class ReadOnlyModelViewSet(RetrieveModelMixin,
                           ListModelMixin,
                           GenericViewSet):
    """
    A viewset that provides default `list()` and `retrieve()` actions.
    """
    pass
