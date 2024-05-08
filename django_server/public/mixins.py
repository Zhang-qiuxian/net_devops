from datetime import datetime

from rest_framework.viewsets import GenericViewSet
from rest_framework.response import Response
from rest_framework.request import Request
from rest_framework.serializers import Serializer
from rest_framework.decorators import action

from django.http import HttpResponse
from django.db.models.query import QuerySet
from django.db.models import Model, Manager
from django.db.models.options import Options
from openpyxl import Workbook

from public.response import ResponseOK, ResponseError
from utils.export_excel import api_export_models, api_export_templates


class CreateModelMixin:
    def create(self, request: Request, *args, **kwargs) -> Response:
        """
        创建单个数据
        """
        serializer: Serializer = self.get_serializer(data=request.data)
        if not serializer.is_valid():
            return ResponseError(message="校验失败!", data=serializer.errors)
        self.perform_create(serializer)
        return ResponseOK(message="创建成功!", data=serializer.data)

    def perform_create(self, serializer: Serializer):
        serializer.save()


class ListModelMixin:
    def list(self, request: Request, *args, **kwargs) -> Response:
        """
        获取多个数据
        """
        queryset: QuerySet = self.filter_queryset(self.get_queryset())
        page = self.paginate_queryset(queryset)
        if page is not None:
            serializer = self.get_serializer(page, many=True)
            return self.get_paginated_response(serializer.data)

        serializer = self.get_serializer(queryset, many=True)
        return ResponseOK(message="查询成功！", data=serializer.data)


class RetrieveModelMixin:

    def retrieve(self, request: Request, *args, **kwargs) -> Response:
        """
        根据 **id** 获取单个数据
        """
        instance = self.get_object()
        serializer = self.get_serializer(instance)
        return ResponseOK(message="查询成功！", data=serializer.data)


class UpdateModelMixin:

    def update(self, request: Request, *args, **kwargs) -> Response:
        """
        更新数据
        """

        partial = kwargs.pop('partial', False)
        instance = self.get_object()
        serializer: Serializer = self.get_serializer(instance, data=request.data, partial=partial)
        if not serializer.is_valid():
            return ResponseError(message="更新失败!", data=serializer.errors, )

        self.perform_update(serializer)

        if getattr(instance, '_prefetched_objects_cache', None):
            # If 'prefetch_related' has been applied to a queryset, we need to
            # forcibly invalidate the prefetch cache on the instance.
            instance._prefetched_objects_cache = {}

        return ResponseOK(message="更新成功!", data=serializer.data)

    def perform_update(self, serializer: Serializer):
        serializer.save()

    def partial_update(self, request: Request, *args, **kwargs) -> Response:
        kwargs['partial'] = True
        return self.update(request, *args, **kwargs)


class DestroyModelMixin:

    def destroy(self, request: Request, *args, **kwargs) -> Response:
        """
        根据 **Id** 删除数据
        """

        instance = self.get_object()
        self.perform_destroy(instance)
        return ResponseOK()

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


class ExportImportMixin:
    exclude_export_fields: list[str] = []
    exclude_import_fields: list[str] = []
    export_models: list[QuerySet[Model]] = []
    templates_model: Model = None

    # @action(methods=['get'], detail=True)
    # def export_excel(self, request: Request, *args, **kwargs) -> HttpResponse:
    #     """
    #     将单个模型导出为excel,如果export_models为空则优先导出本model
    #     :param request:
    #     :param args:
    #     :param kwargs:
    #     :return:
    #     """
    #     pk: str | int = kwargs.get('pk')
    #     obj: QuerySet[Model] = self.get_queryset().filter(pk=pk)
    #     if not obj:
    #         return ResponseError(message="没有数据可以导出！")
    #     if not self.export_models:
    #         response: HttpResponse = api_export_models(models=[obj], exclude=self.exclude_export)
    #         return response
    #     models: list[QuerySet[Model]] = [m.objects.all().order_by('id') for m in self.export_models]
    #     response: HttpResponse = api_export_models(models=[*models, obj], exclude=self.exclude_export)
    #     return response

    @action(methods=['get'], detail=False)
    def export_excel(self, request: Request, *args, **kwargs) -> HttpResponse:
        """
        导出export_model和本models为excel
        要在类中定义exclude_export_fields，排除不需要导出的字段
        export_models，需要导出的modle
        :param request:
        :param args:
        :param kwargs:
        :return:
        """
        obj: QuerySet[Model] = self.get_queryset()
        if not obj:
            return ResponseError(message="没有数据可以导出！")
        if not self.export_models:
            response: HttpResponse = api_export_models(models=[obj], exclude=self.exclude_export_fields)
            return response
        models: list[QuerySet[Model]] = [m.objects.all().order_by('id') for m in self.export_models]
        response: HttpResponse = api_export_models(models=[*models, obj], exclude=self.exclude_export_fields)
        return response

    @action(methods=['get'], detail=False)
    def export_excel_templates(self, request: Request, *args, **kwargs) -> HttpResponse:
        """
        导出model批量导入模板
        要在类中定义exclude_import_fields，排除不需要导入的字段
        :param request:
        :param args:
        :param kwargs:
        :return:
        """
        obj: QuerySet[Model] = self.get_queryset()
        response: HttpResponse = api_export_templates(model=obj[0], exclude=self.exclude_import_fields)
        return response

    @action(methods=['post'], detail=False)
    def import_excel(self, request: Request, *args, **kwargs) -> Response:
        #TODO:导入功能还未实现

        raise NotImplementedError("功能还没未实现")
