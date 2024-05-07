from unittest import case
from warnings import warn
from typing import Any
import pandas as pd

from tools.snmp.scan import bulk_walk, get


def handle_tojson(data: dict[str, list]) -> list[dict]:
    """数据处理"""
    try:
        df = pd.DataFrame(data)
        to_json = df.to_dict(orient="records")
        return to_json
    except Exception as e:
        return []


def handle_mac(data: list[str]) -> list[str]:
    """处理mac地址"""
    return [i.strip('"').replace(" ", ":").lower()[:-1] for i in data]


def handel_symbol_list(data: list[str]) -> list[str]:
    """处理字符串"""
    return [i.strip('"') for i in data]


def handel_ints(data: list[str]) -> list[int]:
    """处理数字"""
    return [int(i) for i in data]


def handel_symbol_dict(data: dict) -> dict:
    """处理字符串"""
    return {k: v[0].strip('"').strip() for k, v in data.items()}


def handel_result(data: Any = None, data_type: str = 'string') -> Any:
    if isinstance(data, list):
        match data_type:
            case 'string':
                return handel_symbol_list(data)
            case 'int':
                return handel_ints(data)
            case 'mac_address':
                return handle_mac(data)
    elif isinstance(data, str):
        match data_type:
            case 'string':
                return data.strip('"')
            case 'int':
                return int(data)
            case 'mac_address':
                return data.strip('"').replace(" ", ":").lower()[:-1]


def start_snmp(**kwargs) -> list[dict] | list:
    """
    格式实例：如果有依赖的index，请添加index的字典
ip_oids = [
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
        ]
    },
]
    :param oids:
    :param kwargs:
    :return:
    """
    oids: list[dict[str, list[dict]]] | None = kwargs.get('oids', None)
    if not oids or not isinstance(oids, list) or len(oids) == 0:
        warn("oids格式不正确")
        return []
    kwargs.pop('oids', None)
    t: dict = {}
    for oid in oids:
        res: list = bulk_walk(oids=oid['oid'], **kwargs)
        data_type: str = oid.get('type')
        dept: str = oid.get('dept')
        t[dept] = handel_result(data=res, data_type=data_type)
        index: list[dict] | None = oid.get('index', None)
        if index:
            for i in index:
                data_type: str = i.get('type')
                dept: str = i.get('dept')
                t[dept] = [handel_result(data=get(oids=f"{i['oid']}.{j}", **kwargs), data_type=data_type)
                           for j in res]
        # print(res)
    dt: list[dict] = handle_tojson(t)
    return dt
