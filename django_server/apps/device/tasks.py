import json
import time
from typing import Callable, Iterator, Any
from concurrent.futures import ThreadPoolExecutor, as_completed, Future

from celery import shared_task
from celery.app.task import Task

from django.db.models import Model, QuerySet

from apps.device.models import Device, DeviceIP, DeviceSystem, DeviceSerial, DeviceInterface, SnmpTemplate
from apps.device.api.serial import SnmpTemplateSerializer

from tools.snmp.run import run

POOL = 50

model_dict: dict[str, Any] = {
    'ip': DeviceIP,
    'system': DeviceSystem,
    'interface': DeviceInterface,
    'serial': DeviceSerial,
}


def update_model(device: Device, datas: list[dict]) -> dict:
    for data in datas:
        for key, value in data.items():
            obj = model_dict[key]
            objs: list[Model] = [obj(**d, device_id=device.device_id, name=device.name, ip=device.ip) for d in value]
            obj.objects.bulk_create(objs=objs)
            device.is_sync = True
            device.save()
        return {"success": {"message": f"{device.ip} 更新完成！"}}


def update_arp(device: Device, datas: list[dict]) -> dict:
    raise ImportError("未实现")


def start_snmp(device: Device, func: Callable = None, oids: None = None) -> dict:
    snmp = SnmpTemplate.objects.get(id=device.snmp_id)
    s_data: dict = SnmpTemplateSerializer(snmp).data
    del_key: list[str] = ['id', 'name']
    s_data: dict = {k: v for k, v in s_data.items() if k not in del_key}
    s_data['hostname'] = device.ip
    s_data['oids'] = oids
    b, r = run(**s_data)
    if not b:
        return r
    return func(device=device, data=r)


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
        res: Iterator[Future] = as_completed([executor.submit(fn=start_snmp, device=d, func=update_model) for d in d_s])
        response = [i.result() for i in res]
        return response


if __name__ == '__main__':
    pass
