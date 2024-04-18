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
from public.mixins import ModelViewSet

from apps.device.models import Device, SnmpTemplate, DeviceCompany
from apps.device.api.seria import (DeviceSerializer, SnmpTemplateSerializer, DeviceCompanySerializer,
                                   DeviceDetailSerializer)

from apps.device.tasks import start_sync


class SnmpTemplateViewSet(ModelViewSet):
    queryset = SnmpTemplate.objects.all().order_by('id')
    serializer_class = SnmpTemplateSerializer


class DeviceCompanyViewSet(ModelViewSet):
    queryset = DeviceCompany.objects.all().order_by('id')
    serializer_class = DeviceCompanySerializer


class DeviceViewSet(ModelViewSet):
    queryset = Device.objects.all().order_by('id')
    serializer_class = DeviceSerializer
    serializer_detail = DeviceDetailSerializer

    def perform_create(self, serializer: Serializer):
        serializer.save()
        start_sync.delay(device=serializer.instance)

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
        df = pandas.read_excel(file.read(), engine='openpyxl')

        return ResponseOK(data={"code": 200, "message": "上传成功", "data": json.loads(df.to_json(orient='records'))})

    @action(methods=['get'], detail=False)
    def export_excel(self, request: Request, *args, **kwargs) -> Response:
        meta = Device._meta
        response: HttpResponse = HttpResponse(content_type='application/ms-excel')
        response['Content-Disposition'] = f'attachment; filename=Export_{datetime.now()}.xlsx'
        # field_names = [field.name for field in meta.fields]
        excel_title = [field.verbose_name for field in meta.fields]
        field_names = [field.name for field in meta.fields]
        wb = Workbook()
        ws = wb.active
        ws.append(field_names)
        # for obj in queryset:
        #     data = [f'{getattr(obj, field)}' for field in field_names]
        #     row = ws.append(data)
        wb.save(response)
        return response


device = DeviceViewSet
device_snmp_templates = SnmpTemplateViewSet
device_company = DeviceCompanyViewSet
