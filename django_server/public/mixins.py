from datetime import datetime

from rest_framework.viewsets import GenericViewSet
from rest_framework.response import Response
from rest_framework.request import Request
from rest_framework.serializers import Serializer
from rest_framework.decorators import action

from django.http import HttpResponse
from django.db.models.query import QuerySet
from openpyxl import Workbook

from public.response import ResponseOK, ResponseError


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
    exclude_export: list[str] = []

    @action(methods=['get'], detail=False)
    def export_excel(self, request: Request, *args, **kwargs) -> Response:
        """
        导出为excel
        :param request:
        :param args:
        :param kwargs:
        :return:
        """
        obj = self.get_queryset()
        if not obj:
            return ResponseError(message="没有数据可以导出！")
        meta = obj[0]._meta
        exclude: list[str] = self.exclude_export
        response: HttpResponse = HttpResponse(content_type='application/ms-excel')
        response['Content-Disposition'] = f'attachment; filename=Export_{datetime.now()}.xlsx'
        # field_names = [field.name for field in meta.fields]
        excel_title = [field.verbose_name for field in meta.fields if field.name not in exclude]
        field_names = [field.name for field in meta.fields if field.name not in exclude]
        wb = Workbook()
        ws = wb.active
        ws.append(excel_title)
        ws.append(field_names)
        for obj in self.queryset:
            data = [f'{getattr(obj, field)}' for field in field_names]
            ws.append(data)
        wb.save(response)
        return response

    def import_excel(self, request: Request, *args, **kwargs) -> Response:
        #TODO:导入功能还未实现

        raise NotImplementedError("功能还没未实现")
