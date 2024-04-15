from rest_framework.serializers import ModelSerializer, IntegerField, UUIDField, SerializerMethodField
from django.db.models import QuerySet

from apps.device.models import Device, SnmpTemplate, DeviceCompany


class DeviceCompanySerializer(ModelSerializer):
    class Meta:
        model = DeviceCompany
        fields = '__all__'


class SnmpTemplateSerializer(ModelSerializer):
    class Meta:
        model = SnmpTemplate
        fields = '__all__'


class DeviceSerializer(ModelSerializer):
    device_id = UUIDField(read_only=True)
    snmp = SerializerMethodField(read_only=True)
    company = SerializerMethodField(read_only=True)
    snmp_id = IntegerField(write_only=True)
    company_id = IntegerField(write_only=True)

    def get_snmp(self, obj: Device):
        s: SnmpTemplate = SnmpTemplate.objects.filter(id=obj.snmp_id).first()
        if s:
            return s.name
        return None

    def get_company(self, obj: Device):
        d: DeviceCompany = DeviceCompany.objects.filter(id=obj.company_id).first()
        if d:
            return d.name
        return None

    class Meta:
        model = Device
        # fields = '__all__'
        exclude = ["id"]
