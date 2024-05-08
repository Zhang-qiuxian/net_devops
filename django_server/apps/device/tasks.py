import json
import time
from typing import Callable, Iterator, Any
from concurrent.futures import ThreadPoolExecutor, as_completed, Future

from celery import shared_task
from celery.app.task import Task

from django.db.models import Model, QuerySet

from apps.device.models import Device, DeviceIP, DeviceSystem, DeviceSerial, DeviceInterface, SnmpTemplate, DeviceARP
from apps.device.api.serial import SnmpTemplateSerializer

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


def update_model(device: Device) -> list[dict]:
    """
    更新ip interface serial system 四个模型
    :param device: Device对象
    :return: 返回完成消息
    """
    b, datas = start_snmp(device=device)
    if not b:
        return datas
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
    return [{"success": {"message": f"{device.ip} 更新完成！"}}]


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
        return response


"""
更新arp
"""


def update_arp(device: Device) -> tuple[bool, list[dict]]:
    """
    更新arp的启动函数
    :param device:
    :return:
    """
    b, datas = start_snmp(device=device, oids=arp_oids)
    datas[0].update({"ip": device.ip, "device_id": device.device_id, "name": device.name})
    return b, datas


def bulk_create_arp(objs: list[DeviceARP]) -> None:
    DeviceARP.objects.bulk_create(objs)


def bulk_update_arp(objs: list[DeviceARP]) -> None:
    DeviceARP.objects.bulk_update(objs=objs, fields=['atPhysAddress', 'atNetAddress', 'update_time'])


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
