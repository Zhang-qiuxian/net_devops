import random
from typing import Callable
import time
import re
from typing import Any, Callable
from unittest import case

from paramiko import SSHClient, AutoAddPolicy, Channel
from paramiko.ssh_exception import AuthenticationException, ChannelException
import logging

logging.basicConfig(level=logging.DEBUG)

ENTER: bytes = b'\n'
CURRENT_CONFIG: bytes = b'display current-configuration'
HUAWEI_SCREEN: bytes = b'screen-length 0 temporary'
H3C_SCREEN: bytes = b'screen-length disable'
H3C_INTERFACE: bytes = b'display interface brief'


def exit_count(func: Callable) -> Callable:
    """
    根据解析次数来返回结果，如果匹配成功次数>5则返回true，如果累计次数>20则返回true
    :param func:
    :return:
    """

    def inner(*args, **kwargs) -> bool:
        f = func(*args, **kwargs)
        inner.all_count += 1
        if not f:
            return f
        inner.count += 1
        if inner.count > 5 or inner.all_count > 20:
            return True

    inner.count = 0
    inner.all_count = 0
    return inner


def disable_screen(c: Channel, device_type: str = None):
    match device_type:
        case None:
            c.close()
            raise Exception("设备类型不能为空")
        case "huawei":
            c.send(HUAWEI_SCREEN + ENTER)
        case "h3c":
            c.send(H3C_SCREEN + ENTER)


def configure_ssh(c: Channel, device_type: str = None):
    if device_type in ["huawei", "h3c"]:
        c.send(CURRENT_CONFIG + ENTER)
        # pass


@exit_count
def re_exit(msg: str, device_type: str = None) -> bool:
    if device_type in ["huawei", "h3c"]:
        r: list = re.findall(r">$|]$", msg)
        if r:
            return True
        else:
            return False


class Connect:
    def __init__(self, hostname: str, username: str, password: str, port: int = 22, device_type: str = None, **kwargs):
        self.hostname: str = hostname
        self.username: str = username
        self.password: str = password
        self.device_type: str = device_type
        self.port: int = port
        self.result: dict = {}
        self._update_att(**kwargs)

    def connect_dispatch(self):
        t, c = self._open()
        if not t:
            return False
        self._screen(c)
        self.result: dict = self._handle_result(data=self._result_data(c))

    @property
    def get_configure(self) -> dict:
        t, c = self._open()
        if not t:
            return self.result
        self._screen(c)
        configure_ssh(c, device_type=self.device_type)
        self.result: dict = self._handle_result(data=self.run_command(c))
        return self.result

    def run_command(self, c: Channel, command: str | bytes) -> str:
        msg: str = ""
        while True:
            temp = c.recv(65535).decode()
            if not temp:
                break
            msg += temp
            c.send(ENTER)
            c.send(command)
            time.sleep(0.5)
            if re_exit(msg=temp, device_type=self.device_type):
                c.close()
                break
        # c.close()
        return msg

    def _screen(self, c: Channel) -> None:
        disable_screen(c, device_type=self.device_type)
        time.sleep(0.5)

    def _open(self) -> tuple[bool, Channel | None]:
        """
        创建ssh连接
        :return:
        """
        self.client = SSHClient()
        self.client.set_missing_host_key_policy(AutoAddPolicy())
        try:
            self.client.connect(hostname=self._get_hostname, username=self.username,
                                password=self.password, port=self.port,
                                look_for_keys=False, timeout=10)
            c: Channel = self.client.invoke_shell()
            return True, c
        except AuthenticationException as au:
            self.result = self._handle_result(code=False, msg="账号密码错误")
            return False, None
        except ChannelException as ce:
            self.result = self._handle_result(code=False, msg="通道异常")
            return False, None
        except TimeoutError as te:
            self.result = self._handle_result(code=False, msg="连接超时")
            return False, None
        except Exception as e:
            self.result = self._handle_result(code=False, msg=str(e))
            return False, None

    def _handle_result(self, code: bool = True, msg: str = "success", data: Any = None) -> dict:
        """
        处理返回值
        :param code:
        :param msg:
        :param data:
        :return:
        """
        return dict(code=code, hostname=self._get_hostname, msg=msg, data=data)

    @property
    def _get_hostname(self) -> str:
        """
        返回设备ip
        :return:
        """
        try:
            ip: str = self.ip
            return ip
        except AttributeError as ae:
            return self.hostname

    def _update_att(self, **kwargs) -> None:
        """
        动态的添加类属性，防止程序报错
        :param kwargs:
        :return:
        """
        for k, v in kwargs.items():
            self.__setattr__(k, v)


if __name__ == '__main__':
    c = Connect('10.10.10.1', username='admin', password='qxxx1473464511mm', port=22, comm="1232423",
                version="v2c", oid="0.0.0.1.0.101", device_type="huawei")
    print(c.__dict__)
    result = c.get_configure
    print(c.__dict__)
