from warnings import warn

from tools.snmp.scan import bulk_walk, get
from tools.snmp.utils import handle_tojson

serial_oids = [
    {
        "dept": "entPhysicalDescr",
        "oid": "1.3.6.1.2.1.47.1.1.1.1.2",
        "func": "实体描述信息"
    },
    {
        "dept": "entPhysicalName",
        "oid": "1.3.6.1.2.1.47.1.1.1.1.7",
        "func": "实体名字"
    },
    {
        "dept": "entPhysicalSerialNum",
        "oid": "1.3.6.1.2.1.47.1.1.1.1.11",
        "func": "实体序列号"
    },
    {
        "dept": "entPhysicalSoftwareRev",
        "oid": "1.3.6.1.2.1.47.1.1.1.1.10",
        "func": "实体软件版本"
    },
    {
        "dept": "entPhysicalModelName",
        "oid": "1.3.6.1.2.1.47.1.1.1.1.13",
        "func": "模型名称"
    },
]

ip_oids = [
    {
        "dept": "ipAdEntAddr",
        "oid": "1.3.6.1.2.1.4.20.1.1",
        "func": "IP地址"
    },
{
        "dept": "ipAdEntNetMask",
        "oid": "1.3.6.1.2.1.4.20.1.3",
        "func": "子网掩码"
    },
    {
        "dept": "ipAdEntIfIndex",
        "oid": "1.3.6.1.2.1.4.20.1.2",
        "func": "接口索引",
        "index": [
            {
                "dept": "ifName",
                "oid": "1.3.6.1.2.1.31.1.1.1.1",
                "func": "接口名字"
            },
            {
                "dept": "ifAlias",
                "oid": "1.3.6.1.2.1.31.1.1.1.18",
                "func": "接口别名"
            },
        ]
    },

]

system_oids = [
    {
        "dept": "sysDescr",
        "oid": "1.3.6.1.2.1.1.1",
        "func": "设备描述"
    },
    {
        "dept": "sysUpTime",
        "oid": "1.3.6.1.2.1.1.3",
        "func": "设备上电时间"
    },
    {
        "dept": "sysName",
        "oid": "1.3.6.1.2.1.1.5",
        "func": "系统名称"
    },
]

interface_oids = [
    {
        "dept": "ifIndex",
        "oid": "1.3.6.1.2.1.2.2.1.1",
        "func": "接口索引"
    },
    {
        "dept": "ifDescr",
        "oid": "1.3.6.1.2.1.2.2.1.2",
        "func": "接口描述"
    },
    {
        "dept": "ifPhysAddress",
        "oid": "1.3.6.1.2.1.2.2.1.6",
        "func": "接口物理地址"
    },
    {
        "dept": "ifOperStatus",
        "oid": "1.3.6.1.2.1.2.2.1.8",
        "func": "接口运行状态"
    },
    {
        "dept": "ifName",
        "oid": "1.3.6.1.2.1.31.1.1.1.1",
        "func": "接口名字"
    },
    {
        "dept": "ifAlias",
        "oid": "1.3.6.1.2.1.31.1.1.1.18",
        "func": "接口别名"
    },
    {
        "dept": "ifHighSpeed",
        "oid": "1.3.6.1.2.1.31.1.1.1.15",
        "func": "接口当前带宽"
    },
]

# class SNMPScanner:
#     def __init__(self, hostname="localhost", version=2, community="public", timeout=20, remote_port=0,
#                  security_level="no_auth_or_privacy", security_username="initial", privacy_protocol="DEFAULT",
#                  privacy_password="", auth_protocol="DEFAULT", auth_password="", context="", use_sprint_value=True):
#         self.hostname = hostname
#         self.version = version
#         self.community = community
#         self.timeout = timeout
#         self.remote_port = remote_port
#         self.security_level = security_level
#         self.security_username = security_username
#         self.privacy_protocol = privacy_protocol
#         self.privacy_password = privacy_password
#         self.auth_protocol = auth_protocol
#         self.auth_password = auth_password
#         self.context = context
#         self.use_sprint_value = use_sprint_value
#         self.update_att()
#
#     @staticmethod
#     def __handle_mac(data: list):
#         """处理mac地址"""
#         return [i.strip('"').replace(" ", ":").lower()[:-1] for i in data]
#
#     @staticmethod
#     def __handel_symbol_list(data: list):
#         """处理字符串"""
#         return [i.strip('"') for i in data]
#
#     @staticmethod
#     def __handel_symbol_dict(data: dict):
#         """处理字符串"""
#         return {k: v[0].strip('"').strip() for k, v in data.items()}
#
#     @property
#     def ip(self) -> list[dict]:
#         rst_dict: dict = {}
#         for oid in _ip_oids:
#             rst_dict[oid['dept']] = bulk_walk()
#
#     def update_att(self, **kwargs):
#         for keyword, value in kwargs.items():
#             if keyword in self.__dict__:
#                 self.__setattr__(keyword, value)
#             else:
#                 warn('Keyword argument "{}" is not an attribute'.format(keyword))


if __name__ == '__main__':
    t: dict = {}
    for oid in ip_oids:
        res: list = bulk_walk(hostname="10.3.11.249", oids=oid['oid'], community="zwy_123", version=2)
        t[oid['dept']] = res
        index: list[dict] | None = oid.get('index', None)
        if index:
            for i in index:
                t[i['dept']] = [get(hostname="10.3.11.249", oids=f"{i['oid']}.{j}", community="zwy_123", version=2)
                                for j in res]

    dt: list[dict] = handle_tojson(t)
    # dt1: list[dict] = []
    # for d in dt:
    #     if d['entPhysicalModelName'] == '':
    #         continue
    #     else:
    #         dt1.append(d)
    print(dt)
