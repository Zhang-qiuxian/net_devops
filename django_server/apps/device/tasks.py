import json
import time
from datetime import datetime
from typing import Callable, Iterator, Any
from concurrent.futures import ThreadPoolExecutor, as_completed, Future
from functools import partial
from itertools import chain

from celery import shared_task
from celery.app.task import Task

from django.db.models import Model, QuerySet
from django.db import transaction

from apps.device.models import Device, DeviceIP, DeviceSystem, DeviceSerial, DeviceInterface, SnmpTemplate, DeviceARP
from apps.device.api.serial import SnmpTemplateSerializer
from apps.cron.models import CronJobSyncLog

from tools.snmp.run import run
from tools.snmp.common import arp_oids

POOL = 50

"""
通用的启动函数
"""

snmp_objs = SnmpTemplate.objects.all()


def start_snmp(device: Device = None, oids: list = None) -> tuple[bool, list[dict]]:
    """
    运行snmp的启动函数
    :param snmps: snmp模板列表
    :param device: Device模型对象
    :param oids: 需要获取的oids列表
    :return: 返回一个元组，第一个值是布尔值标识是否完成，第二个值是获取到的数据
    (True,  [{'serial': [
{'entPhysicalDescr': 'HUAWEI S5720 Routing Switch', 'entPhysicalName': 'HUAWEI S5720 Routing Switch',
 'entPhysicalSerialNum': '2102350BDQDML5000621', 'entPhysicalSoftwareRev': 'Version 5.170 V200R019C10SPC500',
 'entPhysicalModelName': ''}]},
{'ip': [{'ipAdEntAddr': '1.1.1.1', 'ipAdEntNetMask': '255.255.255.255', 'ipAdEntIfIndex': 43, 'ifName': 'LoopBack0',
 'ifAlias': '', 'ifOperStatus': 1}]},
{'system': [{'sysDescr': 'S5720-36PC-EI-AC','sysUpTime': '17:13:37:00.37','sysName': 'zhangqiuxian'}]},
{'interface': [{'ifIndex': 1, 'ifDescr': 'InLoopBack0', 'ifPhysAddress': '00:00:00:00:00:00', 'ifOperStatus': 1,
'ifName': 'InLoopBack0', 'ifAlias': '', 'ifHighSpeed': 0}]}])
    """
    if snmp_objs is None or len(snmp_objs) == 0:
        return False, [{"success": {"message": f"{device.ip} SNMP模板未配置！"}}]
    snmps: list[dict] = SnmpTemplateSerializer(snmp_objs, many=True).data
    snmp = [s for s in snmps if s['id'] == device.snmp_id]
    if len(snmp) == 0:
        return False, [{"success": {"message": f"{device.ip} SNMP模板关联失败！"}}]
    del_key: list[str] = ['id', 'name']
    s_data: dict = {k: v for k, v in snmp[0].items() if k not in del_key}
    s_data['hostname'] = device.ip
    s_data['oids'] = oids
    b, datas = run(**s_data)
    datas[0].update({"ip": device.ip, "device_id": device.device_id.__str__(), "name": device.name})
    return b, datas


def bulk_create(model: Model, objs: list[Model]) -> None:
    """
    批量创建
    :param model:
    :param objs:
    :return:
    """
    model.objects.bulk_create(objs)


def bulk_update(model: Model, objs: list[Model], fields: list[str]) -> None:
    """
    批量更新
    :param model:
    :param objs:
    :param fields:
    :return:
    """
    model.objects.bulk_update(objs=objs, fields=fields)


def start_thread_pool(fn: Callable, queryset: QuerySet[Model]) -> list[tuple[bool, list[dict]]]:
    with ThreadPoolExecutor(max_workers=POOL) as executor:
        res: Iterator[Future] = as_completed([executor.submit(fn, q) for q in queryset])
        response = [i.result() for i in res]
        return response


"""
更新IP interface serial system
"""
model_dict: dict[str, Any] = {
    'ip': DeviceIP,
    'system': DeviceSystem,
    'interface': DeviceInterface,
    'serial': DeviceSerial,
}


def update_model(device: Device) -> tuple[bool, list[dict]]:
    """
    更新ip interface serial system 四个模型
    :param device: Device对象
    :return:
    """

    return start_snmp(device=device, oids=None)
    # if not b:
    #     return b, datas
    # ip: list[DeviceIP] = []
    # interface: list[DeviceInterface] = []
    # serial: list[DeviceSerial] = []
    # system: list[DeviceSystem] = []
    # for data in datas:
    #     for key, value in data.items():
    #         obj = model_dict[key]
    #         match key:
    #             case 'serial':
    #                 serial += [obj(**d, device_id=device.device_id, name=device.name, ip=device.ip) for d in value if
    #                            d['entPhysicalSerialNum'] != '']
    #             case 'interface':
    #                 interface += [obj(**d, device_id=device.device_id, name=device.name, ip=device.ip) for d in value]
    #             case 'seria':
    #                 interface += [obj(**d, device_id=device.device_id, name=device.name, ip=device.ip) for d in value]
    #             case 'system':
    #                 interface += [obj(**d, device_id=device.device_id, name=device.name, ip=device.ip) for d in value]
    # device.is_sync = True
    # device.save()
    # return True, [{"success": {"message": f"{device.ip} 更新完成！"}}]


@shared_task
def start_sync(*args, **kwargs) -> Task | dict:
    """
    同步ip interface serial system
    :param args:
    :param kwargs:
    :return:
    """
    d_q: QuerySet[Device] = Device.objects.filter(is_sync=False).all()
    if len(d_q) == 0:
        return {"success": True, "message": "所有设备都已同步！"}
    response: list[tuple[bool, list[dict]]] = start_thread_pool(fn=run_arp, queryset=d_q)
    fault_list: list[dict] = []
    error_list: list[dict] = []
    success_list: list[dict] = []
    create_ip: list[DeviceIP] = []
    create_interface: list[DeviceInterface] = []
    create_serial: list[DeviceSerial] = []
    create_system: list[DeviceSystem] = []
    for r in response:
        b, m = r
        if not b:
            error_list = error_list+m
        else:
            success_list = success_list+m
    CronJobSyncLog.objects.create(job="同步基础信息", data=success_list)
    return {"success": True, "message": f"成功了{len(success_list)}台,失败了{len(error_list)}台,未获取到{len(fault_list)}台"}


"""
更新arp
"""


def run_arp(device: Device) -> tuple[bool, list[dict]]:
    """
    更新ip interface serial system 四个模型
    :param device: Device对象
    :return:
    """
    return start_snmp(device=device, oids=arp_oids)


@shared_task
def start_sync_arp(*args, **kwargs) -> Task | dict:
    d_q: QuerySet[Device] = Device.objects.filter(is_sync=False).all()
    a_q: QuerySet[DeviceARP] = DeviceARP.objects.all()
    response: list[tuple[bool, list[dict]]] = start_thread_pool(fn=run_arp, queryset=d_q)
    fault_list: list[dict] = []
    error_list: list[dict] = []
    success_list: list[dict] = []
    update_models: list[DeviceARP] = []
    update_status: list[DeviceARP] = []
    create_models: list[DeviceARP] = []
    for res in response:
        b, datas = res
        if not b:
            error_list = error_list + datas
        else:
            arp_list: list[dict] = datas[0].get('arp')
            if len(arp_list) == 0:
                fault_list = fault_list + datas
            else:
                device_id: str = datas[0].get('device_id')
                ip: str = datas[0].get('ip')
                name: str = datas[0].get('name')
                aq: [DeviceARP] = a_q.filter(device_id=device_id)
                if len(aq) == 0:
                    create_models = create_models + [DeviceARP(**a, device_id=device_id, name=name, ip=ip) for a in
                                                     arp_list]
                    success_list = success_list + datas
                else:
                    for q in aq:
                        is_exist: bool = False
                        for di, a in enumerate(arp_list):
                            if q.atNetAddress != a['atNetAddress']:
                                continue
                            else:
                                q.atPhysAddress = a['atPhysAddress']
                                q.atIfIndex = a['atIfIndex']
                                q.ifName = a['ifName']
                                q.ifAlias = a['ifAlias']
                                q.ifOperStatus = a['ifOperStatus']
                                q.is_active = True
                                q.update_time = datetime.now()
                                arp_list.pop(di)
                                update_models.append(q)
                                is_exist = True
                        if not is_exist:
                            q.is_active = False
                            q.update_time = datetime.now()
                            update_status.append(q)
                            is_exist = False
                    if len(arp_list) > 0:
                        create_models = create_models + [DeviceARP(**a, device_id=device_id, name=name, ip=ip)
                                                         for a in arp_list]
                    success_list = success_list + datas
    if len(update_models) > 0:
        fields: list[str] = ['atIfIndex', 'atPhysAddress', 'atNetAddress', 'ifName', 'ifAlias', 'ifOperStatus',
                             'is_active', 'update_time']
        bulk_update(model=DeviceARP, objs=update_models, fields=fields)
    if len(update_status) > 0:
        fields: list[str] = ['is_active', 'update_time']
        bulk_update(model=DeviceARP, objs=update_status, fields=fields)
    if len(create_models) > 0:
        bulk_create(model=DeviceARP, objs=create_models)
    CronJobSyncLog.objects.create(job="更新ARP", data=success_list)
    return {"success": True, "message": f"成功了{len(success_list)}台,失败了{len(error_list)}台,未获取到{len(fault_list)}台"}


if __name__ == '__main__':
    pass
