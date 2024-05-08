import json
import time
from warnings import warn
from typing import Any

from easysnmp.exceptions import EasySNMPError

from tools.snmp.common import standard_oids, arp_oids
from tools.snmp.utils import start_snmp


class SnmpRunner:
    def __init__(self, *args, **kwargs):
        self._update_att(**kwargs)

    def run(self, *args, **kwargs) -> list[dict]:
        self._get_oids(**kwargs)
        return start_snmp(**self._get_att)

    @property
    def run_standard(self) -> list[dict]:
        result: list[dict] = []
        for oid in standard_oids:
            for k, v in oid.items():
                result.append({k: self.run(oids=v)})
        return result

    # @property
    # def ip(self) -> list[dict]:
    #     return self.run(oids=ip_oids)
    #
    # @property
    # def interface(self) -> list[dict]:
    #     return self.run(oids=interface_oids)
    #
    # @property
    # def system(self) -> list[dict]:
    #     return self.run(oids=system_oids)
    #
    # @property
    # def serial(self) -> list[dict]:
    #     data: list[dict] = self.run(oids=serial_oids)
    #     return [i for i in data if i['entPhysicalSerialNum'] != '']

    def _get_oids(self, **kwargs) -> dict:
        oids: list[dict] | None = kwargs.get('oids')
        if oids:
            self.oids = oids

    @property
    def _get_att(self) -> dict:
        return self.__dict__

    def _update_att(self, **kwargs):
        for keyword, value in kwargs.items():
            setattr(self, keyword, value)


# scan_list: list[str] = ['ip', 'interface', 'system', 'serial']


def run(*args, **kwargs) -> tuple[bool, list[dict[str, list | str]]]:
    result: list[dict] = []
    oids = kwargs.get('oids', None)
    runner = SnmpRunner(*args, **kwargs)
    try:
        if oids:
            if isinstance(oids, list):
                for oid in oids:
                    if isinstance(oid, dict):
                        for k, v in oid.items():
                            result.append({k: runner.run(oids=v)})
        else:
            result = runner.run_standard
        return True, result
    except Exception as e:
        if isinstance(e, EasySNMPError):
            return False, [{'error': f"ip:{kwargs.get('hostname')} 请检查SNMP配置"}]
        return False, [{'error': f"ip:{kwargs.get('hostname')} {str(e)}"}]


if __name__ == '__main__':
    # s = SnmpRunner(**{"hostname": '10.232.254.8', "community": 'ch123', "version": 2, "oids": ip_oids})
    # # print(s.ip)
    # # print(s.interface)
    # # print(s.serial)
    # # print(s.system)
    # # print("1111111111111")
    # # print(s.__dict__)
    # print(s.run())
    # print(getattr(s, 'system'))
    # print(s.run())
    # s.ip
    # s.interface
    # s.serial
    # s.system
    # s.run()
    for i in range(3):
        t1 = time.perf_counter()
        temp: dict = {'version': 2, 'community': 'zwy_123', 'security_username': 'user', 'auth_password': 'pass',
                      'auth_protocol': 'MD5', 'security_level': 'noAuthNoPriv', 'privacy_protocol': 'DES',
                      'privacy_password': 'otherPass', 'context': 'context', 'hostname': '10.254.11.249'}
        d,r = run(**temp, oids=arp_oids)
        print(r)
        print(time.perf_counter() - t1)
        time.sleep(3)
