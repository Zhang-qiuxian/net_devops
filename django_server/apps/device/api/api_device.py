import pandas
import json
from rest_framework.request import Request
from rest_framework.response import Response
from rest_framework.decorators import action
from rest_framework.serializers import Serializer

from django.core.files.uploadedfile import TemporaryUploadedFile
from datetime import datetime

from openpyxl import Workbook
from django.http import HttpResponse, JsonResponse
from django.db.models import QuerySet

from public.response import ResponseOK, ResponseError
from public.mixins import ModelViewSet, ReadOnlyModelViewSet, ExportImportMixin

from apps.device.models import Device, SnmpTemplate, DeviceCompany, DeviceSystem, DeviceIP, DeviceSerial, \
    DeviceInterface
from apps.device.api.seria import (DeviceSerializer, SnmpTemplateSerializer, DeviceCompanySerializer,
                                   DeviceDetailSerializer, DeviceSystemSerializer, DeviceIPSerializer,
                                   DeviceSerialSerializer, DeviceInterfaceSerializer)


class DeviceInterfaceViewSet(ExportImportMixin, ReadOnlyModelViewSet):
    queryset = DeviceInterface.objects.all().order_by('id')
    serializer_class = DeviceInterfaceSerializer
    exclude_export: list[str] = ['id']

    def retrieve(self, request: Request, *args, **kwargs) -> Response:
        """
        根据设备的 **device_id** 获取单个设备接口的信息
        """
        pk: str = kwargs.get('pk')
        if not pk:
            return ResponseError(message="请携带设备id！")
        d: Device = self.queryset.filter(device_id=pk).all()
        if not d:
            return ResponseError(message="设备id不存在！")
        serializer = self.serializer_class(d, many=True)
        return ResponseOK(message="查询成功！", data=serializer.data)


class DeviceSerialViewSet(ExportImportMixin, ReadOnlyModelViewSet):
    queryset = DeviceSerial.objects.all().order_by('id')
    serializer_class = DeviceSerialSerializer
    exclude_export: list[str] = ['id']

    def retrieve(self, request: Request, *args, **kwargs) -> Response:
        pk: str = kwargs.get('pk')
        if not pk:
            return ResponseError(message="请携带设备id！")
        d: Device = self.queryset.filter(device_id=pk).all()
        if not d:
            return ResponseError(message="设备id不存在！")
        serializer = self.serializer_class(d, many=True)
        return ResponseOK(message="查询成功！", data=serializer.data)


class DeviceIPViewSet(ExportImportMixin, ReadOnlyModelViewSet):
    queryset = DeviceIP.objects.all().order_by('id')
    serializer_class = DeviceIPSerializer
    exclude_export: list[str] = ['id']

    def retrieve(self, request: Request, *args, **kwargs) -> Response:
        pk: str = kwargs.get('pk')
        if not pk:
            return ResponseError(message="请携带设备id！")
        d: Device = self.queryset.filter(device_id=pk).all()
        if not d:
            return ResponseError(message="设备id不存在！")
        serializer = self.serializer_class(d, many=True)
        return ResponseOK(message="查询成功！", data=serializer.data)


class DeviceSystemViewSet(ExportImportMixin, ReadOnlyModelViewSet):
    queryset = DeviceSystem.objects.all().order_by('id')
    serializer_class = DeviceSystemSerializer
    exclude_export: list[str] = ['id']

    def retrieve(self, request: Request, *args, **kwargs) -> Response:
        pk: str = kwargs.get('pk')
        if not pk:
            return ResponseError(message="请携带设备id！")
        d: Device = self.queryset.filter(device_id=pk).first()
        if not d:
            return ResponseError(message="设备id不存在！")
        serializer = self.serializer_class(d, many=False)
        return ResponseOK(message="查询成功！", data=serializer.data)


class SnmpTemplateViewSet(ModelViewSet):
    queryset = SnmpTemplate.objects.all().order_by('id')
    serializer_class = SnmpTemplateSerializer


class DeviceCompanyViewSet(ModelViewSet):
    queryset = DeviceCompany.objects.all().order_by('id')
    serializer_class = DeviceCompanySerializer


class DeviceViewSet(ExportImportMixin, ModelViewSet):
    queryset: QuerySet[Device] = Device.objects.all().order_by('id')
    serializer_class = DeviceSerializer
    serializer_detail = DeviceDetailSerializer
    exclude_export: list[str] = ['id', 'is_sync']

    def perform_create(self, serializer: Serializer):
        serializer.save()
        # start_sync.delay(device=serializer.instance)

    def retrieve(self, request: Request, *args, **kwargs) -> Response:
        pk: str = kwargs.get('pk')
        if not pk:
            return ResponseError(message="请携带设备id！")
        d: Device = self.queryset.filter(device_id=pk).first()
        if not d:
            return ResponseError(message="设备id不存在！")
        sa = self.serializer_detail(instance=d)
        return ResponseOK(data=sa.data)

    @action(methods=['post'], detail=False)
    def upload(self, request: Request, *args, **kwargs) -> Response:
        file: TemporaryUploadedFile = request.FILES.get('file')
        file_type: list[str] = ['xlsx', 'csv', 'xls']
        if not file:
            return ResponseError(message="添加失败,请上传文件。")
        if file.name.split('.')[-1] not in file_type:
            return ResponseError(message="添加失败,文件格式不正确。请添加xlsx/csv/xls")
        df = pandas.read_excel(file.read(), engine='openpyxl')
        d_d: list[dict] = df.to_dict(orient='records')
        db_ip: list = []
        db_hostname: list = []
        for d in self.queryset:
            db_ip.append(d.ip)
            db_hostname.append(d.hostname)
        is_eq: list = [e for e in d_d if e['ip'] in db_ip or e['hostname'] in db_hostname]
        if not is_eq:
            objs: [Device] = [Device(**d) for d in d_d]
            Device.objects.bulk_create(objs=objs)
            return ResponseOK(message=f"添加成功,添加了{len(d_d)}台设备")
        return ResponseError(message="添加失败,请删除重复设备后再添加", data=is_eq)


device = DeviceViewSet
device_snmp_templates = SnmpTemplateViewSet
device_company = DeviceCompanyViewSet
device_ip = DeviceIPViewSet
device_system = DeviceSystemViewSet
device_serial = DeviceSerialViewSet
device_interface = DeviceInterfaceViewSet
