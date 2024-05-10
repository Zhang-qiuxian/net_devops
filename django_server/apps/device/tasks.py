import json
import time
from datetime import datetime
from typing import Callable, Iterator, Any
from concurrent.futures import ThreadPoolExecutor, as_completed, Future

from celery import shared_task
from celery.app.task import Task

from django.db.models import Model, QuerySet

from apps.device.models import Device, DeviceIP, DeviceSystem, DeviceSerial, DeviceInterface, SnmpTemplate, DeviceARP
from apps.device.api.serial import SnmpTemplateSerializer
from apps.cron.models import CronJobSyncLog

from tools.snmp.run import run
from tools.snmp.common import arp_oids

POOL = 50

"""
通用的启动函数
"""


def start_snmp(device: Device, oids: list[dict] = None) -> tuple[bool, list[dict]]:
    """
    运行snmp的启动函数
    :param device: Device模型对象
    :param oids: 需要获取的oids列表
    :return: 返回一个元组，第一个值是布尔值标识是否完成，第二个值是获取到的数据
    """
    snmp = SnmpTemplate.objects.filter(id=device.snmp_id).first()
    if not snmp:
        return False, [{"success": {"message": f"{device.ip} SNMP模板关联失败！"}}]
    s_data: dict = SnmpTemplateSerializer(snmp).data
    del_key: list[str] = ['id', 'name']
    s_data: dict = {k: v for k, v in s_data.items() if k not in del_key}
    s_data['hostname'] = device.ip
    s_data['oids'] = oids
    return run(**s_data)


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
    :return: 返回完成消息
    """
    b, datas = start_snmp(device=device)
    if not b:
        return b, datas
    for data in datas:
        for key, value in data.items():
            obj = model_dict[key]
            if key == 'serial':
                objs: list[Model] = [obj(**d, device_id=device.device_id, name=device.name, ip=device.ip)
                                     for d in value if d['entPhysicalSerialNum'] != '']
            else:
                objs: list[Model] = [obj(**d, device_id=device.device_id, name=device.name, ip=device.ip) for d in
                                     value]
            obj.objects.bulk_create(objs=objs)
        device.is_sync = True
        device.save()
    return True, [{"success": {"message": f"{device.ip} 更新完成！"}}]


@shared_task
def start_sync(*args, **kwargs) -> Task:
    """
    同步ip interface serial system
    :param args:
    :param kwargs:
    :return:
    """
    d_s: QuerySet[Device] = Device.objects.filter(is_sync=False).all()
    if len(d_s) == 0:
        return {"success": True, "message": "所有设备都已同步！"}

    with ThreadPoolExecutor(max_workers=POOL) as executor:
        res: Iterator[Future] = as_completed([executor.submit(update_model, device=d) for d in d_s])
        response = [i.result() for i in res]
        error: int = 0
        success: int = 0
        success_list: list[dict] = []
        for r in response:
            b, m = r
            if not b:
                error += 1
            else:
                success += 1
                success_list.append(m)
        CronJobSyncLog.objects.create(job="同步基础信息", data=success_list)
        return {"error": f"失败了{error}台", "success": f"成功了{success}台"}


"""
更新arp
"""


def update_arp(device: Device) -> tuple[bool, list[dict]]:
    """
    更新arp的启动函数
    :param device:
    :return: [{
    'arp': [{
    'atIfIndex': 4, 'ifName': 'MEth0/0/1', 'ifAlias': '', 'ifOperStatus': 2, 'atNetAddress': '192.168.255.253',
    'atPhysAddress': 'f4:de:af:4e:b7:f0'},
    {'atIfIndex': 39, 'ifName': 'Vlanif10', 'ifAlias': '', 'ifOperStatus': 1, 'atNetAddress': '10.10.10.29',
    'atPhysAddress': '54:ee:75:96:f9:1a'
    }],
    'ip': '10.10.10.1', 'device_id': UUID('19a4d7fc-11c6-44e9-857a-94782763a870'),
    'name': 'test'
    }]
    """
    b, datas = start_snmp(device=device, oids=arp_oids)
    datas[0].update({"ip": device.ip, "device_id": device.device_id, "name": device.name})
    return b, datas


def bulk_create_arp(objs: list[DeviceARP]) -> None:
    DeviceARP.objects.bulk_create(objs)


def bulk_update_arp(objs: list[DeviceARP]) -> None:
    fields: list[str] = ['atPhysAddress', 'atNetAddress', 'update_time']
    DeviceARP.objects.bulk_update(objs=objs, fields=fields)


def handle_arp(new_datas: list[dict], queryset: list[DeviceARP]) -> None:
    error_list: list[dict] = []
    success_list: list[dict] = []
    update_interface_list: list[DeviceARP] = []
    update_mac_list: list[DeviceARP] = []
    update_active_list: list[DeviceARP] = []
    create_list: list[DeviceARP] = []

    arps: list[dict] | None = new_datas[0].get('arp', None)
    if arps is None or len(arps) == 0:
        error_list.append(new_datas[0])
        return
    ip: str = arps[0].get('ip')
    device_id: str = arps[0].get('device_id')
    name: str = arps[0].get('name')
    for q in queryset:
        for i, a in enumerate(arps):
            if q.atNetAddress == a['atNetAddress'] and q.atPhysAddress == a['atPhysAddress']:
                q.atIfIndex = a['atIfIndex']
                q.ifName = a['ifName']
                q.ifAlias = a['ifAlias']
                q.ifOperStatus = a['ifOperStatus']
                q.is_active = True
                q.update_time = datetime.now()
                update_interface_list.append(q)
                arps.pop(i)
            elif q.atNetAddress == a['atNetAddress'] and q.atPhysAddress != a['atPhysAddress']:
                q.atIfIndex = a['atIfIndex']
                q.ifName = a['ifName']
                q.ifAlias = a['ifAlias']
                q.atPhysAddress = a['atPhysAddress']
                q.ifOperStatus = a['ifOperStatus']
                q.is_active = True
                q.update_time = datetime.now()
                update_mac_list.append(q)
                arps.pop(i)
            else:
                update_active_list.append(q)
                arps.pop(i)
    if len(arps) > 0:
        create_list = [DeviceARP(**a, ip=ip, name=name, device_id=device_id) for a in arps]


@shared_task
def start_sync_arp(*args, **kwargs) -> Task:
    d_q: QuerySet[Device] = Device.objects.filter(is_sync=True).all()
    a_q: QuerySet[DeviceARP] = DeviceARP.objects.all()
    with ThreadPoolExecutor(max_workers=POOL) as executor:
        res: Iterator[Future] = as_completed([executor.submit(update_arp, device=d) for d in d_q])
        response: list[tuple] = [i.result() for i in res]
    fault_list: list[dict] = []
    error_list: list[dict] = []
    success_list: list[dict] = []
    for res in response:
        b, datas = res
        if not b:
            error_list.append(datas)
        else:
            arp_list: list[dict] = datas[0].get('arp')
            if len(arp_list) == 0:
                fault_list.append(datas)
            else:
                device_id: str = datas[0].get('device_id')
                ip: str = datas[0].get('ip')
                name: str = datas[0].get('name')
                aq: [DeviceARP] = a_q.filter(device_id=device_id)
                if not aq:
                    objs: list[DeviceARP] = [DeviceARP(**a, device_id=device_id, name=name, ip=ip) for a in arp_list]
                    bulk_create_arp(objs=objs)
                    success_list.append(datas)
                else:
                    # is_exist_ip: list[str] = [i.ip for i in aq]
                    # new_ip_obj: list[DeviceARP] = []
                    # is_exist_obj: list[DeviceARP] = []
                    # for a_obj in aq:
                    #     if a_obj.ip in is_exist_ip:
                    #         is_exist_obj.append(DeviceARP(**a_i))
                    #     else:
                    #         new_ip_obj.append(DeviceARP(**a_i))
                    # bulk_create_arp(objs=new_ip_obj)
                    # bulk_update_arp(objs=is_exist_obj)
                    # success_list.append(datas)
                    pass
    return {"success": success_list, "fault_list": fault_list, "error_list": error_list}


if __name__ == '__main__':
    pass
