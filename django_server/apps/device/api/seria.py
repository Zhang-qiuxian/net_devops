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
    system_queryset: QuerySet[DeviceSystem] = DeviceSystem.objects.all().order_by('id')
    device_id = UUIDField(read_only=True)
    snmp_id = IntegerField(write_only=True)
    company_id = IntegerField(write_only=True)
    system = SerializerMethodField(read_only=True, required=False)

    def get_system(self, obj: Device):
        s: [QuerySet] = [s for s in self.system_queryset if s.device_id == obj.device_id]
        return DeviceSystemSerializer(instance=s, many=True).data

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


# class DeviceDetailSerializer(ModelSerializer):
#     device_id = UUIDField(read_only=True, required=False)
#     # snmp = SerializerMethodField(read_only=True)
#     # company = SerializerMethodField(read_only=True)
#     # ip = SerializerMethodField(read_only=True)
#     # serial = SerializerMethodField(read_only=True)
#     system = SerializerMethodField(read_only=True)
#     # interface = SerializerMethodField(read_only=True)
#
#     # def get_snmp(self, obj: Device):
#     #     s: SnmpTemplate = SnmpTemplate.objects.filter(id=obj.snmp_id).first()
#     #     if s:
#     #         return SnmpTemplateSerializer(instance=s).data
#     #     return None
#
#     # def get_company(self, obj: Device):
#     #     d: DeviceCompany = DeviceCompany.objects.filter(id=obj.company_id).first()
#     #     if d:
#     #         return DeviceCompanySerializer(instance=d).data
#     #     return None
#
#     # def get_ip(self, obj: Device):
#     #     i: QuerySet = DeviceIP.objects.filter(device_id=obj.device_id).all()
#     #     if not i:
#     #         return None
#     #     return DeviceIPSerializer(instance=i, many=True).data
#
#     def get_serial(self, obj: Device):
#         s: QuerySet = DeviceSerial.objects.filter(device_id=obj.device_id).all()
#         if not s:
#             return None
#         return DeviceSerialSerializer(instance=s, many=True).data
#
#     def get_system(self, obj: Device):
#         s: DeviceSystem = DeviceSystem.objects.filter(device_id=obj.device_id).all()
#         return DeviceSystemSerializer(instance=s, many=True).data
#
#     # def get_interface(self, obj: Device):
#     #     i: QuerySet = DeviceInterface.objects.filter(device_id=obj.device_id).all()
#     #     if not i:
#     #         return None
#     #     return DeviceInterfaceSerializer(instance=i, many=True).data
#
#     class Meta:
#         model = Device
#         exclude = ["id"]

class DeviceDetailSerializer(ModelSerializer):
    ip_queryset: QuerySet[DeviceIP] = DeviceIP.objects.all().order_by('id')
    system_queryset: QuerySet[DeviceSystem] = DeviceSystem.objects.all().order_by('id')
    interface_queryset: QuerySet[DeviceInterface] = DeviceInterface.objects.all().order_by('id')
    serial_queryset: QuerySet[DeviceSerial] = DeviceSerial.objects.all().order_by('id')
    snmp_queryset: QuerySet[SnmpTemplate] = SnmpTemplate.objects.all().order_by('id')
    company_queryset: QuerySet[DeviceCompany] = DeviceCompany.objects.all().order_by('id')

    device_id = UUIDField(read_only=True, required=False)
    snmp = SerializerMethodField(read_only=True)
    company = SerializerMethodField(read_only=True)
    ip = SerializerMethodField(read_only=True)
    serial = SerializerMethodField(read_only=True)
    system = SerializerMethodField(read_only=True)
    interface = SerializerMethodField(read_only=True)

    def get_snmp(self, obj: Device):
        s: [SnmpTemplate] = [s for s in self.snmp_queryset if s.id == obj.snmp_id]
        return SnmpTemplateSerializer(instance=s, many=True).data

    def get_company(self, obj: Device):
        d: [DeviceCompany] = [c for c in self.company_queryset if c.id == obj.company_id]
        return DeviceCompanySerializer(instance=d, many=True).data

    def get_ip(self, obj: Device):
        i: [QuerySet] = [i for i in self.ip_queryset if i.device_id == obj.device_id]
        return DeviceIPSerializer(instance=i, many=True).data

    def get_serial(self, obj: Device):
        s: [QuerySet] = [s for s in self.serial_queryset if s.device_id == obj.device_id]
        return DeviceSerialSerializer(instance=s, many=True).data

    def get_system(self, obj: Device):
        s: [QuerySet] = [s for s in self.system_queryset if s.device_id == obj.device_id]
        return DeviceSystemSerializer(instance=s, many=True).data

    def get_interface(self, obj: Device):
        i: [QuerySet] = [i for i in self.interface_queryset if i.device_id == obj.device_id]
        return DeviceInterfaceSerializer(instance=i, many=True).data

    class Meta:
        model = Device
        exclude = ["id"]


class DeviceExportSerializer(ModelSerializer):
    ip_queryset: QuerySet[DeviceIP] = DeviceIP.objects.all().order_by('id')
    system_queryset: QuerySet[DeviceSystem] = DeviceSystem.objects.all().order_by('id')
    interface_queryset: QuerySet[DeviceInterface] = DeviceInterface.objects.all().order_by('id')
    serial_queryset: QuerySet[DeviceSerial] = DeviceSerial.objects.all().order_by('id')
    snmp_queryset: QuerySet[SnmpTemplate] = SnmpTemplate.objects.all().order_by('id')
    company_queryset: QuerySet[DeviceCompany] = DeviceCompany.objects.all().order_by('id')

    device_id = UUIDField(read_only=True, required=False)
    snmp = SerializerMethodField(read_only=True)
    company = SerializerMethodField(read_only=True)
    ip = SerializerMethodField(read_only=True)
    serial = SerializerMethodField(read_only=True)
    system = SerializerMethodField(read_only=True)
    interface = SerializerMethodField(read_only=True)

    def get_snmp(self, obj: Device):
        s: [SnmpTemplate] = [s for s in self.snmp_queryset if s.id == obj.snmp_id]
        return s

    def get_company(self, obj: Device):
        d: [DeviceCompany] = [c for c in self.company_queryset if c.id == obj.company_id]
        return d

    def get_ip(self, obj: Device):
        i: [QuerySet] = [i for i in self.ip_queryset if i.device_id == obj.device_id]
        return i

    def get_serial(self, obj: Device):
        s: [QuerySet] = [s for s in self.serial_queryset if s.device_id == obj.device_id]
        return s

    def get_system(self, obj: Device):
        s: [QuerySet] = [s for s in self.system_queryset if s.device_id == obj.device_id]
        return s

    def get_interface(self, obj: Device):
        i: [QuerySet] = [i for i in self.interface_queryset if i.device_id == obj.device_id]
        return i

    class Meta:
        model = Device
        exclude = ["id"]
