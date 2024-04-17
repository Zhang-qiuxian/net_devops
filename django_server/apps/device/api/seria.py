from rest_framework.serializers import ModelSerializer, IntegerField, UUIDField, SerializerMethodField
from django.db.models import QuerySet

from apps.device.models import Device, SnmpTemplate, DeviceCompany, DeviceIP, DeviceSerial, DeviceSystem, \
    DeviceInterface


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
    # snmp = SerializerMethodField(read_only=True)
    # company = SerializerMethodField(read_only=True)
    snmp_id = IntegerField(write_only=True)
    company_id = IntegerField(write_only=True)

    # def get_snmp(self, obj: Device):
    #     s: SnmpTemplate = SnmpTemplate.objects.filter(id=obj.snmp_id).first()
    #     if s:
    #         return s.name
    #     return None
    #
    # def get_company(self, obj: Device):
    #     d: DeviceCompany = DeviceCompany.objects.filter(id=obj.company_id).first()
    #     if d:
    #         return d.name
    #     return None

    class Meta:
        model = Device
        # fields = '__all__'
        exclude = ["id"]


class DeviceIPSerializer(ModelSerializer):
    class Meta:
        model = DeviceIP
        fields = '__all__'


class DeviceSerialSerializer(ModelSerializer):
    class Meta:
        model = DeviceSerial
        fields = '__all__'


class DeviceSystemSerializer(ModelSerializer):
    class Meta:
        model = DeviceSystem
        fields = '__all__'


class DeviceInterfaceSerializer(ModelSerializer):
    class Meta:
        model = DeviceInterface
        fields = '__all__'


class DeviceDetailSerializer(ModelSerializer):
    device_id = UUIDField(read_only=True, required=False)
    snmp = SerializerMethodField(read_only=True)
    company = SerializerMethodField(read_only=True)
    ip = SerializerMethodField(read_only=True)
    serial = SerializerMethodField(read_only=True)
    system = SerializerMethodField(read_only=True)
    interface = SerializerMethodField(read_only=True)

    def get_snmp(self, obj: Device):
        s: SnmpTemplate = SnmpTemplate.objects.filter(id=obj.snmp_id).first()
        if s:
            return SnmpTemplateSerializer(instance=s).data
        return None

    def get_company(self, obj: Device):
        d: DeviceCompany = DeviceCompany.objects.filter(id=obj.company_id).first()
        if d:
            return DeviceCompanySerializer(instance=d).data
        return None

    def get_ip(self, obj: Device):
        i: QuerySet = DeviceIP.objects.filter(id=obj.device_id).all()
        if not i:
            return None
        if len(i) > 1:
            return DeviceIPSerializer(instance=i, many=True).data
        return DeviceIPSerializer(instance=i, many=False).data

    def get_serial(self, obj: Device):
        s: QuerySet = DeviceSerial.objects.filter(device_id=obj.device_id).all()
        if not s:
            return None
        if len(s) > 1:
            return DeviceSerialSerializer(instance=s, many=True).data
        return DeviceSerialSerializer(instance=s, many=False).data

    def get_system(self, obj: Device):
        s: QuerySet = DeviceSystem.objects.filter(device_id=obj.device_id).all()
        if not s:
            return None
        if len(s) > 1:
            return DeviceSystemSerializer(instance=s, many=True).data
        return DeviceSystemSerializer(instance=s, many=False).data

    def get_interface(self, obj: Device):
        i: QuerySet = DeviceInterface.objects.filter(device_id=obj.device_id).all()
        if not i:
            return None
        if len(i) > 1:
            return DeviceInterfaceSerializer(instance=i, many=True).data
        return DeviceInterfaceSerializer(instance=i, many=False).data

    class Meta:
        model = Device
        exclude = ["id"]
