from public.mixins import ModelViewSet

from apps.device.models import Device, SnmpTemplate, DeviceCompany
from apps.device.api.seria import DeviceSerializer, SnmpTemplateSerializer, DeviceCompanySerializer


class SnmpTemplateViewSet(ModelViewSet):
    queryset = SnmpTemplate.objects.all().order_by('id')
    serializer_class = SnmpTemplateSerializer


class DeviceCompanyViewSet(ModelViewSet):
    queryset = DeviceCompany.objects.all().order_by('id')
    serializer_class = DeviceCompanySerializer


class DeviceViewSet(ModelViewSet):
    queryset = Device.objects.all().order_by('id')
    serializer_class = DeviceSerializer


device = DeviceViewSet
device_snmp_templates = SnmpTemplateViewSet
device_company = DeviceCompanyViewSet
