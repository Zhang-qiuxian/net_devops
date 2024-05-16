# 标准的oids，获取系统信息、设备接口、设备接口IP、设备序列号
standard_oids: [list[dict[str:list[dict[str:str | list]]]]] = [
    {
        'serial': [
            {
                "dept": "entPhysicalDescr",
                "oid": "1.3.6.1.2.1.47.1.1.1.1.2",
                "func": "实体描述信息",
                "type": "string"
            },
            {
                "dept": "entPhysicalName",
                "oid": "1.3.6.1.2.1.47.1.1.1.1.7",
                "func": "实体名字",
                "type": "string"
            },
            {
                "dept": "entPhysicalSerialNum",
                "oid": "1.3.6.1.2.1.47.1.1.1.1.11",
                "func": "实体序列号",
                "type": "string"
            },
            {
                "dept": "entPhysicalSoftwareRev",
                "oid": "1.3.6.1.2.1.47.1.1.1.1.10",
                "func": "实体软件版本",
                "type": "string"
            },
            {
                "dept": "entPhysicalModelName",
                "oid": "1.3.6.1.2.1.47.1.1.1.1.13",
                "func": "模型名称",
                "type": "string"
            },
        ],
    },
    {
        'ip': [
            {
                "dept": "ipAdEntAddr",
                "oid": "1.3.6.1.2.1.4.20.1.1",
                "func": "IP地址",
                "type": "string"
            },
            {
                "dept": "ipAdEntNetMask",
                "oid": "1.3.6.1.2.1.4.20.1.3",
                "func": "子网掩码",
                "type": "string"
            },
            {
                "dept": "ipAdEntIfIndex",
                "oid": "1.3.6.1.2.1.4.20.1.2",
                "func": "接口索引",
                "type": "int",
                "index": [
                    {
                        "dept": "ifName",
                        "oid": "1.3.6.1.2.1.31.1.1.1.1",
                        "func": "接口名字",
                        "type": "string"
                    },
                    {
                        "dept": "ifAlias",
                        "oid": "1.3.6.1.2.1.31.1.1.1.18",
                        "func": "接口别名",
                        "type": "string"
                    },
                    {
                        "dept": "ifOperStatus",
                        "oid": "1.3.6.1.2.1.2.2.1.8",
                        "func": "接口运行状态",
                        "type": "int"
                    },
                ]
            },

        ],
    },
    {
        'system': [
            {
                "dept": "sysDescr",
                "oid": "1.3.6.1.2.1.1.1",
                "func": "设备描述",
                "type": "string"
            },
            {
                "dept": "sysUpTime",
                "oid": "1.3.6.1.2.1.1.3",
                "func": "设备上电时间",
                "type": "string"
            },
            {
                "dept": "sysName",
                "oid": "1.3.6.1.2.1.1.5",
                "func": "系统名称",
                "type": "string"
            },
        ],
    },
    {
        'interface': [
            {
                "dept": "ifIndex",
                "oid": "1.3.6.1.2.1.2.2.1.1",
                "func": "接口索引",
                "type": "int"
            },
            {
                "dept": "ifDescr",
                "oid": "1.3.6.1.2.1.2.2.1.2",
                "func": "接口描述",
                "type": "string"
            },
            {
                "dept": "ifPhysAddress",
                "oid": "1.3.6.1.2.1.2.2.1.6",
                "func": "接口物理地址",
                "type": "mac_address"
            },
            {
                "dept": "ifOperStatus",
                "oid": "1.3.6.1.2.1.2.2.1.8",
                "func": "接口运行状态",
                "type": "int"
            },
            {
                "dept": "ifName",
                "oid": "1.3.6.1.2.1.31.1.1.1.1",
                "func": "接口名字",
                "type": "string"
            },
            {
                "dept": "ifAlias",
                "oid": "1.3.6.1.2.1.31.1.1.1.18",
                "func": "接口别名",
                "type": "string"
            },
            {
                "dept": "ifHighSpeed",
                "oid": "1.3.6.1.2.1.31.1.1.1.15",
                "func": "接口当前带宽",
                "type": "int"
            },
        ]
    }
]

# arp oid RFC1213-MIB
arp_oids: list[dict[str:list[dict[str:str | list]]]] = [
    {
        'arp': [
            {
                "dept": "ipNetToMediaIfIndex",
                "oid": "1.3.6.1.2.1.4.22.1.1",
                "func": "接口索引",
                "type": "int",
                "index": [
                    {
                        "dept": "ifName",
                        "oid": "1.3.6.1.2.1.31.1.1.1.1",
                        "func": "接口名字",
                        "type": "string"
                    },
                    {
                        "dept": "ifAlias",
                        "oid": "1.3.6.1.2.1.31.1.1.1.18",
                        "func": "接口别名",
                        "type": "string"
                    },
                    {
                        "dept": "ifOperStatus",
                        "oid": "1.3.6.1.2.1.2.2.1.8",
                        "func": "接口运行状态",
                        "type": "int"
                    },
                ]
            },
            {
                "dept": "ipNetToMediaNetAddress",
                "oid": "1.3.6.1.2.1.4.22.1.3",
                "func": "IP地址",
                "type": "string"
            },
            {
                "dept": "ipNetToMediaPhysAddress",
                "oid": "1.3.6.1.2.1.4.22.1.2",
                "func": "MAC地址",
                "type": "mac_address"
            },
        ]
    }
]
