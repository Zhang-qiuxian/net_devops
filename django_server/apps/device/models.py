import uuid

from django.db import models


class Device(models.Model):
    """
    设备信息
    """
    device_id = models.UUIDField(default=uuid.uuid4, editable=False, verbose_name="设备id", db_comment="设备id")
    name = models.CharField(max_length=32, verbose_name="设备名称", db_comment="设备名称")
    description = models.CharField(max_length=255, blank=True, null=True, verbose_name="设备描述",
                                   db_comment="设备描述")
    hostname = models.CharField(unique=True, max_length=32, verbose_name="主机名", db_comment="主机名")
    ip = models.GenericIPAddressField(unique=True, verbose_name="设备ip", db_comment="设备ip")
    login = models.CharField(max_length=32, verbose_name="登录方式", db_comment="登录方式")
    url = models.CharField(default='-', max_length=128, blank=True, null=True, verbose_name="网址", db_comment="网址")
    username = models.CharField(max_length=32, verbose_name="账号", db_comment="账号")
    password = models.CharField(max_length=64, verbose_name="密码", db_comment="密码")
    remark = models.TextField(default='-', blank=True, null=True, verbose_name="备注", db_comment="备注")
    snmp_id = models.IntegerField(default=1, verbose_name="snmp模板id", db_comment="snmp模板id")
    company_id = models.IntegerField(default=1, verbose_name="设备厂商id", db_comment="设备厂商id")
    create_time = models.DateTimeField(auto_now_add=True, verbose_name="创建时间", db_comment="创建时间")
    update_time = models.DateTimeField(auto_now=True, verbose_name="更新时间", db_comment="更新时间")
    is_sync = models.BooleanField(default=0, verbose_name="是否同步", db_comment="是否同步")

    def __str__(self):
        return self.name

    class Meta:
        db_table = 'device'
        verbose_name = '设备表'
        verbose_name_plural = verbose_name
        db_table_comment = '设备模型'
        ordering = ['-id']


class SnmpTemplate(models.Model):
    """
    snmp模板
    """
    name = models.CharField(unique=True, max_length=32, verbose_name="模板名", db_comment="模板名")
    version = models.IntegerField(default=2, verbose_name="版本", db_comment="版本")
    community = models.CharField(max_length=32, default="public", verbose_name="团体字", db_comment="团体字")
    security_username = models.CharField(max_length=32, default="user", blank=True, null=True, verbose_name="用户名",
                                         db_comment="用户名")
    auth_password = models.CharField(max_length=32, default="pass", blank=True, null=True, verbose_name="密码",
                                     db_comment="密码")
    auth_protocol = models.CharField(max_length=32, default="MD5", blank=True, null=True, verbose_name="认证协议",
                                     db_comment="认证协议")
    security_level = models.CharField(max_length=32, default="noAuthNoPriv", blank=True, null=True,
                                      verbose_name="认证级别", db_comment="认证级别")
    privacy_protocol = models.CharField(max_length=32, default="DES", blank=True, null=True, verbose_name="私有协议",
                                        db_comment="私有协议")
    privacy_password = models.CharField(max_length=32, default="otherPass", blank=True, null=True,
                                        verbose_name="私有密码", db_comment="私有密码")
    context = models.CharField(max_length=32, default="context", blank=True, null=True, verbose_name="上下文",
                               db_comment="上下文")

    def __str__(self):
        return self.name

    class Meta:
        db_table = 'device_snmp_template'
        verbose_name = 'snmp模板'
        verbose_name_plural = verbose_name
        db_table_comment = 'snmp模板'
        ordering = ['id']


class DeviceInterface(models.Model):
    """
    设备接口
    """
    device_id = models.UUIDField(editable=False, verbose_name="设备id", db_comment="设备id")
    name = models.CharField(max_length=32, verbose_name="设备名称", db_comment="设备名称")
    ip = models.GenericIPAddressField(verbose_name="设备ip", db_comment="设备ip")
    ifIndex = models.IntegerField(verbose_name="接口索引", db_comment="接口索引")
    ifDescr = models.CharField(max_length=32, verbose_name="描述接口的字符串", db_comment="描述接口的字符串")
    ifPhysAddress = models.CharField(max_length=32, verbose_name="MAC地址", db_comment="MAC地址")
    ifOperStatus = models.IntegerField(verbose_name="接口当前的状态", db_comment="接口当前的状态")
    ifName = models.CharField(max_length=32, verbose_name="接口名", db_comment="接口名")
    ifAlias = models.CharField(max_length=32, verbose_name="接口别名", db_comment="接口别名")
    ifHighSpeed = models.IntegerField(verbose_name="接口当前带宽", db_comment="接口当前带宽")

    def __str__(self):
        return self.ifDescr

    class Meta:
        db_table = 'device_interface'
        verbose_name = '设备接口'
        verbose_name_plural = verbose_name
        db_table_comment = '设备接口'
        ordering = ['id']


class DeviceIP(models.Model):
    """
    设备ip
    """
    device_id = models.UUIDField(editable=False, verbose_name="设备id", db_comment="设备id")
    name = models.CharField(max_length=32, verbose_name="设备名称", db_comment="设备名称")
    ip = models.GenericIPAddressField(verbose_name="设备ip", db_comment="设备ip")
    ipAdEntAddr = models.GenericIPAddressField(verbose_name="IP地址", db_comment="IP地址")
    ipAdEntIfIndex = models.IntegerField(verbose_name="接口的索引值", db_comment="接口的索引值")
    ipAdEntNetMask = models.GenericIPAddressField(verbose_name="子网掩码", db_comment="子网掩码")
    ifName = models.CharField(max_length=32, verbose_name="接口名", db_comment="接口名")
    ifAlias = models.CharField(max_length=32, verbose_name="接口别名", db_comment="接口别名")

    def __str__(self):
        return self.ipAdEntAddr

    class Meta:
        db_table = 'device_ip'
        verbose_name = '设备ip'
        verbose_name_plural = verbose_name
        db_table_comment = '设备ip'
        ordering = ['id']


class DeviceSystem(models.Model):
    """
    设备系统信息
    """
    device_id = models.UUIDField(editable=False, verbose_name="设备id", db_comment="设备id")
    name = models.CharField(max_length=32, verbose_name="设备名称", db_comment="设备名称")
    ip = models.GenericIPAddressField(verbose_name="设备ip", db_comment="设备ip")
    sysDescr = models.CharField(max_length=128, verbose_name="系统的文字描述", db_comment="系统的文字描述")
    sysUpTime = models.CharField(max_length=32, verbose_name="运行的时间", db_comment="运行的时间")
    sysName = models.CharField(max_length=128, verbose_name="hostname", db_comment="hostname")

    def __str__(self):
        return self.sysName

    class Meta:
        db_table = 'device_system'
        verbose_name = '设备系统信息'
        verbose_name_plural = verbose_name
        db_table_comment = '设备系统信息'
        ordering = ['id']


class DeviceSerial(models.Model):
    """
    设备系统信息
    """
    device_id = models.UUIDField(editable=False, verbose_name="设备id", db_comment="设备id")
    name = models.CharField(max_length=32, verbose_name="设备名称", db_comment="设备名称")
    ip = models.GenericIPAddressField(verbose_name="设备ip", db_comment="设备ip")
    entPhysicalDescr = models.CharField(max_length=128, verbose_name="物理实体描述信息", db_comment="物理实体描述信息")
    entPhysicalName = models.CharField(max_length=128, verbose_name="实体名字", db_comment="实体名字")
    entPhysicalSerialNum = models.CharField(max_length=128, verbose_name="序列号", db_comment="序列号")
    entPhysicalSoftwareRev = models.CharField(max_length=128, verbose_name="软件版本号", db_comment="软件版本号")
    entPhysicalModelName = models.CharField(max_length=128, verbose_name="模型名称", db_comment="模型名称")

    def __str__(self):
        return self.entPhysicalName

    class Meta:
        db_table = 'device_serial'
        verbose_name = '设备系统信息'
        verbose_name_plural = verbose_name
        db_table_comment = '设备系统信息'
        ordering = ['id']


class DeviceCompany(models.Model):
    """
    设备厂家信息
    """
    code = models.CharField(max_length=32, verbose_name="厂家代码", db_comment="厂家代码")
    name = models.CharField(max_length=32, verbose_name="厂家名称", db_comment="厂家名称")
    model = models.CharField(max_length=32, unique=True, verbose_name="设备型号", db_comment="设备型号")

    def __str__(self):
        return self.code

    class Meta:
        db_table = 'device_company'
        verbose_name = '设备厂家信息'
        verbose_name_plural = verbose_name
        db_table_comment = '设备厂家信息'
        ordering = ['id']
