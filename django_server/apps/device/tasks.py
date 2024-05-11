import json
import time
from datetime import datetime
from typing import Callable, Iterator, Any
from concurrent.futures import ThreadPoolExecutor, as_completed, Future

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


def start_snmp(device: Device, snmps: list[dict] = None, oids: list[dict] = None) -> tuple[bool, list[dict]]:
    """
    运行snmp的启动函数
    :param snmps: snmp模板列表
    :param device: Device模型对象
    :param oids: 需要获取的oids列表
    :return: 返回一个元组，第一个值是布尔值标识是否完成，第二个值是获取到的数据
    """
    if snmps is None or len(snmps) == 0:
        return False, [{"success": {"message": f"{device.ip} SNMP模板未配置！"}}]
    snmp = [s for s in snmps if s['id'] == device.snmp_id]
    if len(snmp) == 0:
        return False, [{"success": {"message": f"{device.ip} SNMP模板关联失败！"}}]
    del_key: list[str] = ['id', 'name']
    s_data: dict = {k: v for k, v in snmp[0].items() if k not in del_key}
    s_data['hostname'] = device.ip
    s_data['oids'] = oids
    return run(**s_data)


def bulk_create(model: Model, objs: list[Model]) -> None:
    model.objects.bulk_create(objs)


def bulk_update(model: Model, objs: list[Model], fields: list[str]) -> None:
    model.objects.bulk_update(objs=objs, fields=fields)


"""
更新IP interface serial system
"""
model_dict: dict[str, Any] = {
    'ip': DeviceIP,
    'system': DeviceSystem,
    'interface': DeviceInterface,
    'serial': DeviceSerial,
}


def update_model(device: Device, snmps: list[dict]) -> tuple[bool, list[dict]]:
    """
    更新ip interface serial system 四个模型
    :param device: Device对象
    :return: 返回完成消息
    """

    return start_snmp(device=device, snmps=snmps, oids=None)
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
    d_s: QuerySet[Device] = Device.objects.filter(is_sync=False).all()
    if len(d_s) == 0:
        return {"success": True, "message": "所有设备都已同步！"}
    snmp = SnmpTemplate.objects.all()
    s_data: dict = SnmpTemplateSerializer(snmp, many=True).data
    with ThreadPoolExecutor(max_workers=POOL) as executor:
        res: Iterator[Future] = as_completed(
            [executor.submit(update_model, **{"device": d, "snmps": s_data}) for d in d_s])
        response = [i.result() for i in res]

        error_list: list[dict] = []
        success_list: list[dict] = []
        ip: list[DeviceIP] = []
        interface: list[DeviceInterface] = []
        serial: list[DeviceSerial] = []
        system: list[DeviceSystem] = []
        for r in response:
            print(r)
            b, m = r
            if not b:
                error_list.append(m)
            else:
                success_list.append(m)
        CronJobSyncLog.objects.create(job="同步基础信息", data=success_list)
        return {"success": True, "message": f"成功了{len(success_list)}台,失败了{len(error_list)}台"}


"""
更新arp
"""


def update_arp(device: Device, snmps: list[dict]) -> tuple[bool, list[dict]]:
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
    b, datas = start_snmp(device=device, snmps=snmps, oids=arp_oids)
    datas[0].update({"ip": device.ip, "device_id": device.device_id.__str__(), "name": device.name})
    return b, datas


# def handel_arp(datas: list[dict], queryset: list[DeviceARP], update_models: list[DeviceARP],
#                update_status: list[DeviceARP], create_models: list[dict]):
#     new_datas: list[dict] = datas
#     for q in queryset:
#         for di, a in enumerate(new_datas):
#             if q.atNetAddress == a['atNetAddress']:
#                 q.atPhysAddress = a['atPhysAddress']
#                 q.atIfIndex = a['atIfIndex']
#                 q.ifName = a['ifName']
#                 q.ifAlias = a['ifAlias']
#                 q.ifOperStatus = a['ifOperStatus']
#                 q.is_active = True
#                 q.update_time = datetime.now()
#                 new_datas.pop(di)
#                 update_models.append(q)
#             else:
#                 q.is_active = False
#                 q.update_time = datetime.now()
#                 update_status.append(q)
#     if len(new_datas) > 0:
#         create_models += new_datas


@shared_task
def start_sync_arp(*args, **kwargs) -> Task | dict:
    d_q: QuerySet[Device] = Device.objects.filter(is_sync=True).all()
    a_q: QuerySet[DeviceARP] = DeviceARP.objects.all()
    snmp = SnmpTemplate.objects.all()
    s_data: dict = SnmpTemplateSerializer(snmp, many=True).data
    with ThreadPoolExecutor(max_workers=POOL) as executor:
        res: Iterator[Future] = as_completed(
            [executor.submit(update_arp, **{"device": d, "snmps": s_data}) for d in d_q])
        response: list[tuple] = [i.result() for i in res]
    fault_list: list[dict] = []
    error_list: list[dict] = []
    success_list: list[dict] = []
    update_models: list[DeviceARP] = []
    update_status: list[DeviceARP] = []
    create_models: list[DeviceARP] = []
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
                    create_models += [DeviceARP(**a, device_id=device_id, name=name, ip=ip) for a in arp_list]
                    success_list.append(datas)
                else:
                    for q in aq:
                        for di, a in enumerate(arp_list):
                            if q.atNetAddress == a['atNetAddress']:
                                q.atPhysAddress = a['atPhysAddress']
                                q.atIfIndex = a['atIfIndex']
                                q.ifName = a['ifName']
                                q.ifAlias = a['ifAlias']
                                q.ifOperStatus = a['ifOperStatus']
                                q.is_active = True
                                q.update_time = datetime.now()
                                arp_list.pop(di)
                                update_models.append(q)
                            else:
                                q.is_active = False
                                q.update_time = datetime.now()
                                update_status.append(q)
                if len(arp_list) > 0:
                    create_models += [DeviceARP(**a, device_id=device_id, name=name, ip=ip) for a in arp_list]
                success_list.append(datas)
    if len(update_models) > 0:
        fields: list[str] = ['atIfIndex', 'atPhysAddress', 'atNetAddress', 'ifName', 'ifAlias', 'ifOperStatus',
                             'is_active', 'update_time']
        bulk_update(objs=update_models, fields=fields,model=DeviceARP)
    if len(update_status) > 0:
        fields: list[str] = ['is_active', 'update_time']
        bulk_update(objs=update_status, fields=fields,model=DeviceARP)
    if len(create_models) > 0:
        bulk_create(objs=create_models,model=DeviceARP)
    CronJobSyncLog.objects.create(job="更新ARP", data=success_list)
    return {"success": True,
            "message": f"成功了{len(success_list)}台,失败了{len(error_list)}台,未获取到{len(fault_list)}台"}


if __name__ == '__main__':
    pass
