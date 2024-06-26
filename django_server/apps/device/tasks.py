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

POOL: int = 20

"""
通用的启动函数
"""


def start_snmp(device: Device = None, oids: list = None) -> tuple[bool, list[dict]]:
    """
    运行snmp的启动函数,返回值示例
    (True, [
    {
        'serial': [{}],
        'device_ip': '1.1.1.1',
        'device_id': 'be541815-1098-47fc-8cbe-cfa84ab6f8ec',
        'device_name': '11F交换机'
    }, {
        'ip': [{}],
        'device_ip': '1.1.1.1',
        'device_id': 'be541815-1098-47fc-8cbe-cfa84ab6f8ec',
        'device_name': '11F交换机'
    }, {
        'system': [{}],
        'device_ip': '1.1.1.1',
        'device_device_id': 'be541815-1098-47fc-8cbe-cfa84ab6f8ec',
        'device_name': '11F交换机'
    }, {
        'interface': [{}],
        'device_ip ': '1.1.1.1',
        'device_device_id ': 'be541815-1098-47fc-8cbe-cfa84ab6f8ec',
        'device_name ': '11F交换机'
    }
])
    :param snmps: snmp模板列表
    :param device: Device模型对象
    :param oids: 需要获取的oids列表
    :return: 返回一个元组，第一个值是布尔值标识是否完成，第二个值是获取到的数据
    """
    snmp_objs = SnmpTemplate.objects.all()
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
    if not b:
        return b, datas
    new_datas: list[dict] = []
    for d in datas:
        d['device_ip'] = device.ip
        d['device_id'] = device.device_id.__str__()
        d['device_name'] = device.name
        new_datas.append(d)
    return b, new_datas


def bulk_create(model: Model, objs: list[Model]) -> None:
    """
    批量创建
    :param model:
    :param objs:
    :return:
    """
    with transaction.atomic():
        model.objects.bulk_create(objs)


def bulk_update(model: Model, objs: list[Model], fields: list[str]) -> None:
    """
    批量更新
    :param model:
    :param objs:
    :param fields:
    :return:
    """
    with transaction.atomic():
        model.objects.bulk_update(objs=objs, fields=fields)


def start_thread_pool(fn: Callable, queryset: QuerySet[Model], /, *args, **kwargs) -> list[tuple[bool, list[dict]]]:
    with ThreadPoolExecutor(max_workers=POOL) as executor:
        res: Iterator[Future] = as_completed([executor.submit(fn, q, *args, **kwargs) for q in queryset])
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


def create_base_model(device: Device) -> tuple[bool, list[dict]]:
    """
    创建ip interface serial system 四个模型
    :param device: Device对象
    :return:
    """
    b, datas = start_snmp(device=device, oids=None)
    if not b:
        return b, datas
    keys: list[str] = ['device_ip', 'device_name', 'device_id']
    for data in datas:
        for key, value in data.items():
            if key in keys:
                pass
            else:
                obj = model_dict[key]
                if key == 'serial':
                    bulk_create(obj, [obj(**d, device_id=device.device_id, name=device.name, ip=device.ip)
                                      for d in value if d['entPhysicalSerialNum'] != ''])
                else:
                    bulk_create(obj, [obj(**d, device_id=device.device_id, name=device.name, ip=device.ip)
                                      for d in value])
    device.is_sync = True
    device.save()
    return True, [{"success": {"message": f"{device.ip} 更新完成！"}}]


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
        return {"job": "更新基础信息",  "message": "所有设备都已同步！"}
    response: list[tuple[bool, list[dict]]] = start_thread_pool(create_base_model, d_q)
    error_count: int = 0
    success_count: int = 0
    for r in response:
        b, m = r
        if not b:
            error_count += 1
        else:
            success_count += 1
    CronJobSyncLog.objects.create(job="同步基础信息", data=response)
    return {"job": "更新基础信息", "message": f"成功了{success_count}台,失败了{error_count}台。"}


"""
更新arp
"""


def run_arp(device: Device) -> tuple[bool, list[dict]]:
    """
    更新arp模型
    :param device: Device对象
    :return:
    """
    return start_snmp(device=device, oids=arp_oids)


@shared_task
def start_sync_arp(*args, **kwargs) -> Task | dict:
    d_q: QuerySet[Device] = Device.objects.filter(is_sync=True).all()
    a_q: QuerySet[DeviceARP] = DeviceARP.objects.all()
    i_q: QuerySet[DeviceInterface] = DeviceInterface.objects.all()
    response: list[tuple[bool, list[dict]]] = start_thread_pool(run_arp, d_q)
    fault_list: list[dict] = []
    error_list: list[dict] = []
    success_list: list[dict] = []
    update_models: list[DeviceARP] = []
    update_status: list[DeviceARP] = []
    create_models: list[DeviceARP] = []

    def bulk_create_model(_arp_list: dict[str:dict], _interface_map: dict[int:DeviceInterface], _name: str, _ip: str,
                          _device_id: str) -> None:
        # 新建arp
        for _, v in _arp_list.items():
            inter_index: int = v['ipNetToMediaIfIndex']
            obj = DeviceARP(ifAlias=_interface_map[inter_index].ifAlias, ifName=_interface_map[inter_index].ifName,
                            device_id=_device_id, name=_name, ip=_ip, **v)
            create_models.append(obj)

    # 遍历每一个设备的值
    for res in response:
        b, datas = res
        if not b:
            error_list.extend(datas)
        else:
            arp_list: list[dict] = datas[0].get('arp')
            if len(arp_list) == 0:
                fault_list.extend(datas)
            else:
                device_id: str = datas[0].get('device_id')
                ip: str = datas[0].get('device_ip')
                name: str = datas[0].get('device_name')
                # 根据device_id筛选出接口表
                iq: QuerySet[DeviceInterface] = i_q.filter(device_id=device_id)
                arp_map: dict[str:dict] = {a['ipNetToMediaNetAddress']: a for a in arp_list}  # 使用字典映射来加速查找
                interface_map: dict[int:DeviceInterface] = {i.ifIndex: i for i in iq}  # 使用字典映射来加速查找
                if not iq.exists():
                    fault_list.append({"message": "基础信息还未同步！", "data": datas})
                else:
                    # 在arp表中过滤出已存在的arp
                    aq: [DeviceARP] = a_q.filter(device_id=device_id)
                    if not aq.exists():
                        # 如果arp中不存在则直接创建arp模型对象
                        bulk_create_model(arp_map, interface_map, _name=name, _ip=ip, _device_id=device_id)
                        success_list.extend(datas)
                    else:
                        # 更新arp
                        for q in aq:
                            ip_address = q.ipNetToMediaNetAddress
                            if ip_address in arp_map:
                                # 更新存在的ARP条目
                                a = arp_map.pop(ip_address)  # 从映射中删除已处理的条目
                                q.ipNetToMediaPhysAddress = a['ipNetToMediaPhysAddress']
                                q.ipNetToMediaIfIndex = a['ipNetToMediaIfIndex']
                                # 更新接口信息
                                if q.ipNetToMediaIfIndex in interface_map:
                                    q.ifName = interface_map[q.ipNetToMediaIfIndex].ifName
                                    q.ifAlias = interface_map[q.ipNetToMediaIfIndex].ifAlias
                                    q.ifOperStatus = interface_map[q.ipNetToMediaIfIndex].ifOperStatus
                                q.is_active = True
                                q.update_time = datetime.now()
                                update_models.append(q)
                            else:
                                # 如果ARP条目不存在，则更新其状态为不活动
                                q.is_active = False
                                q.update_time = datetime.now()
                                update_status.append(q)
                        if arp_map:
                            bulk_create_model(arp_map, interface_map, _name=name, _ip=ip, _device_id=device_id)
                        success_list.extend(datas)
    if len(update_models) > 0:
        fields: list[str] = ['ipNetToMediaIfIndex', 'ipNetToMediaIfIndex', 'ipNetToMediaNetAddress', 'ifName',
                             'ifAlias', 'ifOperStatus', 'is_active', 'update_time']
        bulk_update(model=DeviceARP, objs=update_models, fields=fields)
    if len(update_status) > 0:
        fields: list[str] = ['is_active', 'update_time']
        bulk_update(model=DeviceARP, objs=update_status, fields=fields)
    if len(create_models) > 0:
        bulk_create(model=DeviceARP, objs=create_models)
    CronJobSyncLog.objects.create(job="更新ARP",
                                  data={"success": success_list, "error": error_list, "fault": fault_list})
    return {"job": "更新ARP",
            "message": f"成功了{len(success_list)}台,失败了{len(error_list)}台,未获取到{len(fault_list)}台"}


if __name__ == '__main__':
    pass
