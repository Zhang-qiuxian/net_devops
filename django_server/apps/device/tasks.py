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

model_dict: dict[str, Any] = {
    'ip': DeviceIP,
    'system': DeviceSystem,
    'interface': DeviceInterface,
    'serial': DeviceSerial,
}


def update_model(device: Device) -> list[dict]:
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


def update_arp(device: Device) -> tuple[bool, list[dict]]:
    # b, datas = start_snmp(device=device, oids=arp_oids)
    return start_snmp(device=device, oids=arp_oids)
    # return [{"success": {"message": f"{device.ip} 更新完成！"}}]


def start_snmp(device: Device, oids: list[dict] = None) -> tuple[bool, list[dict]]:
    snmp = SnmpTemplate.objects.filter(id=device.snmp_id).first()
    if not snmp:
        return False, [{"success": {"message": f"{device.ip} SNMP模板关联失败！"}}]
    s_data: dict = SnmpTemplateSerializer(snmp).data
    del_key: list[str] = ['id', 'name']
    s_data: dict = {k: v for k, v in s_data.items() if k not in del_key}
    s_data['hostname'] = device.ip
    s_data['oids'] = oids
    return run(**s_data)


@shared_task
def add(x, y) -> Task:
    print("task----------111111----------")
    time.sleep(5)
    return x + y


@shared_task
def start_sync(*args, **kwargs) -> Task:
    d_s: QuerySet[Device] = Device.objects.filter(is_sync=False).all()
    if len(d_s) == 0:
        return {"success": True, "message": "所有设备都已同步！"}

    with ThreadPoolExecutor(max_workers=POOL) as executor:
        res: Iterator[Future] = as_completed([executor.submit(update_model, device=d) for d in d_s])
        response = [i.result() for i in res]
        return response


@shared_task
def start_sync_arp(*args, **kwargs) -> Task:
    d_s: QuerySet[Device] = Device.objects.all()
    with ThreadPoolExecutor(max_workers=POOL) as executor:
        res: Iterator[Future] = as_completed([executor.submit(update_arp, device=d) for d in d_s])
        response = [i.result() for i in res]
    return response


if __name__ == '__main__':
    pass
