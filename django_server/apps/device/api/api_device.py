from datetime import datetime
from io import BytesIO
import pandas
from rest_framework.request import Request
from rest_framework.response import Response
from rest_framework.decorators import action
from rest_framework.serializers import Serializer
from rest_framework.utils.serializer_helpers import ReturnDict

from django.core.files.uploadedfile import TemporaryUploadedFile
from django.db.models import QuerySet, Manager, Model

from django.http import HttpResponse

from public.response import ResponseOK, ResponseError
from public.mixins import ModelViewSet, ReadOnlyModelViewSet, ExportMixin, ExportTemplateMixin, CreateModelMixin

from apps.device.models import Device, SnmpTemplate, DeviceCompany, DeviceSystem, DeviceIP, DeviceSerial, \
    DeviceInterface, DeviceARP
from apps.device.api.serial import (DeviceSerializer, SnmpTemplateSerializer, DeviceCompanySerializer,
                                    DeviceDetailSerializer, DeviceSystemSerializer, DeviceIPSerializer,
                                    DeviceSerialSerializer, DeviceInterfaceSerializer, DeviceExportSerializer,
                                    DeviceArpSerializer)


# from rest_framework.filters import SearchFilter, OrderingFilter
# from django_filters.rest_framework import DjangoFilterBackend


class DeviceInterfaceViewSet(ExportMixin, ReadOnlyModelViewSet):
    queryset = DeviceInterface.objects.all().order_by('id')
    serializer_class = DeviceInterfaceSerializer
    exclude_export_fields: list[str] = ['id', 'device_id']
    filterset_fields = ['device_id', 'name', 'ip']

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


class DeviceSerialViewSet(ExportMixin, ReadOnlyModelViewSet):
    queryset = DeviceSerial.objects.all().order_by('id')
    serializer_class = DeviceSerialSerializer
    filterset_fields = ['device_id', 'name', 'ip']
    exclude_export_fields: list[str] = ['id', 'device_id']

    def retrieve(self, request: Request, *args, **kwargs) -> Response:
        pk: str = kwargs.get('pk')
        if not pk:
            return ResponseError(message="请携带设备id！")
        d: Device = self.queryset.filter(device_id=pk).all()
        if not d:
            return ResponseError(message="设备id不存在！")
        serializer = self.serializer_class(d, many=True)
        return ResponseOK(message="查询成功！", data=serializer.data)


class DeviceIPViewSet(ExportMixin, ReadOnlyModelViewSet):
    queryset = DeviceIP.objects.all().order_by('id')
    serializer_class = DeviceIPSerializer
    filterset_fields = ['device_id', 'name', 'ip', 'ipAdEntAddr', 'ifName']
    exclude_export_fields: list[str] = ['id', 'device_id']

    def retrieve(self, request: Request, *args, **kwargs) -> Response:
        pk: str = kwargs.get('pk')
        if not pk:
            return ResponseError(message="请携带设备id！")
        d: Device = self.queryset.filter(device_id=pk).all()
        if not d:
            return ResponseError(message="设备id不存在！")
        serializer = self.serializer_class(d, many=True)
        return ResponseOK(message="查询成功！", data=serializer.data)


class DeviceSystemViewSet(ExportMixin, ReadOnlyModelViewSet):
    queryset = DeviceSystem.objects.all().order_by('id')
    serializer_class = DeviceSystemSerializer
    exclude_export_fields: list[str] = ['id', 'device_id']
    filterset_fields = ['device_id', 'name', 'ip']

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
    filterset_fields = ['id', 'name']


class DeviceCompanyViewSet(ModelViewSet):
    queryset = DeviceCompany.objects.all().order_by('id')
    serializer_class = DeviceCompanySerializer


class DeviceARPViewSet(ExportMixin, ReadOnlyModelViewSet):
    queryset = DeviceARP.objects.all().order_by('id')
    serializer_class = DeviceArpSerializer
    search_fields: list[str] = ['atPhysAddress', 'atNetAddress']
    # 导入导出相关
    filterset_fields = ['device_id', 'name', 'ip', 'ifName', 'atNetAddress']
    exclude_export_fields: list[str] = ['id', 'device_id']

    def retrieve(self, request: Request, *args, **kwargs) -> Response:
        pk: str = kwargs.get('pk')
        if not pk:
            return ResponseError(message="请携带设备id！")
        d: Device = self.queryset.filter(device_id=pk).all()
        if not d:
            return ResponseError(message="设备id不存在！")
        serializer = self.serializer_class(d, many=True)
        return ResponseOK(message="查询成功！", data=serializer.data)


class DeviceViewSet(ExportMixin, ExportTemplateMixin, ReadOnlyModelViewSet, CreateModelMixin):
    queryset: QuerySet[Device] = Device.objects.all().order_by('id')
    serializer_class = DeviceSerializer
    serializer_detail = DeviceDetailSerializer
    serializer_export = DeviceExportSerializer
    exclude_export_fields: list[str] = ['id', 'is_sync']
    # export_models: list[Model] = [DeviceIP, DeviceSystem, DeviceSerial, DeviceInterface]
    templates_model = Device
    exclude_import_fields: list[str] = ['id', 'is_sync', 'create_time', 'update_time', 'device_id']
    filterset_fields = ['device_id', 'name', 'ip']
    templates_tip_list = [
        "导入时务必将**第一行**和**第二行**删除之后再导入！snmp_id和company_id要和snmp模板，设备厂家的序号对应得上，否则同步失败如果有空值请填写 * 或者 -"]

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

    def update(self, request: Request, *args, **kwargs) -> Response:
        """
        更新数据
        """
        pk: str = kwargs.get('pk')
        partial = kwargs.pop('partial', False)
        instance = self.queryset.filter(device_id=pk).first()
        serializer: Serializer = self.get_serializer(instance, data=request.data, partial=partial)
        if not serializer.is_valid():
            return ResponseError(message="更新失败!", data=serializer.errors)

        self.perform_update(serializer)

        if getattr(instance, '_prefetched_objects_cache', None):
            # If 'prefetch_related' has been applied to a queryset, we need to
            # forcibly invalidate the prefetch cache on the instance.
            instance._prefetched_objects_cache = {}

        return ResponseOK(message="更新成功!", data=serializer.data)

    @action(detail=False, methods=['post'])
    def delete(self, request: Request, *args, **kwargs):
        """
       根据device_id列表删除数据
       """
        data: dict = request.data
        device_ids: list = data.get('device_ids', [])
        if len(device_ids) == 0:
            return ResponseError(message="请传入设备id")
        instance = self.queryset.filter(device_id__in=device_ids)
        instance.delete()
        delete_models: list[Model] = [DeviceIP, DeviceSystem, DeviceSerial, DeviceInterface, DeviceARP]
        for model in delete_models:
            model.objects.filter(device_id__in=device_ids).delete()
        return ResponseOK(message="删除成功!")

    @action(methods=['post'], detail=False)
    def import_excel(self, request: Request, *args, **kwargs) -> Response:
        file: TemporaryUploadedFile = request.FILES.get('file')
        if not file:
            return ResponseError(message="添加失败,请上传文件。")
        file_types: list[str] = ['xlsx', 'csv', 'xls']
        file_type: str = file.name.split('.')[-1]
        if file_type not in file_types:
            return ResponseError(message="添加失败,文件格式不正确。请添加xlsx/csv/xls")
        io_file = BytesIO(file.read())
        match file_type:
            case 'xlsx':
                df = pandas.read_excel(io_file, engine='openpyxl')
            case 'xls':
                df = pandas.read_excel(io_file, engine='openpyxl')
            case 'csv':
                df = pandas.read_csv(io_file)
        d_d: list[dict] = df.to_dict(orient='records')
        if len(d_d) == 0:
            return ResponseError(message="添加失败！请检查模板文件格式是否错误！")
        db_ip: list = []
        db_hostname: list = []
        try:
            for d in self.queryset:
                db_ip.append(d.ip)
                db_hostname.append(d.hostname)
            is_eq: list[dict] = []
            is_not_eq: list[dict] = []
            for e in d_d:
                if e['ip'] in db_ip or e['hostname'] in db_hostname:
                    is_eq.append(e)
                else:
                    is_not_eq.append(e)
            if is_not_eq:
                objs: [Device] = [Device(**d) for d in is_not_eq]
                Device.objects.bulk_create(objs=objs)
                return ResponseOK(message=f"添加成功,添加了{len(is_not_eq)}台设备")
            return ResponseError(message="添加失败,请删除重复设备后再添加", data=is_eq)
        except Exception as e:
            return ResponseError(message=f"添加失败，详细错误{str(e)}")


device = DeviceViewSet
device_snmp_templates = SnmpTemplateViewSet
device_company = DeviceCompanyViewSet
device_ip = DeviceIPViewSet
device_system = DeviceSystemViewSet
device_serial = DeviceSerialViewSet
device_interface = DeviceInterfaceViewSet
device_arp = DeviceARPViewSet
