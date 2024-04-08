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

    def get_snmp(self, obj: Device):
        s: QuerySet = SnmpTemplate.objects.filter(id=obj.snmp_id).first()
        return SnmpTemplateSerializer(instance=s).data

    def get_company(self, obj: Device):
        d: QuerySet = DeviceCompany.objects.filter(id=obj.company_id).first()
        return DeviceCompanySerializer(instance=d).data

    class Meta:
        model = Device
        # fields = '__all__'
        exclude = ["id"]
