import os
import random
from typing import Callable
import time
import re
from typing import Any, Callable, Dict
from unittest import case
import sys

from paramiko import SSHClient, AutoAddPolicy, Channel
from paramiko.ssh_exception import AuthenticationException, ChannelException
import logging

logging.basicConfig(level=logging.DEBUG)

ENTER: bytes = '\n'.encode()
CURRENT_CONFIG: str = 'display current-configuration'
# CURRENT_CONFIG: str = 'display current-configuration'
HUAWEI_SCREEN: bytes = b'screen-length 0 temporary'
H3C_SCREEN: bytes = b'screen-length disable'
H3C_INTERFACE: bytes = b'display interface brief'
HH_SAVE: bytes = b'save force'


def exit_count(func: Callable[..., Any]) -> Callable[..., bool]:
    """
    根据解析次数来返回结果，如果匹配成功次数>5则返回True，如果累计次数>40则返回True
    :param func: 要装饰的函数
    :return: 装饰后的函数
    """

    def inner(*args, **kwargs) -> bool:
        nonlocal count, all_count  # 声明 count 和 all_count 为非局部变量
        result = func(*args, **kwargs)  # 调用原始函数并存储其返回值
        all_count += 1  # 所有调用次数加1
        if result:  # 如果原始函数返回 False（或等价于 False 的值）
            count += 1  # 匹配成功次数加1
        # 如果匹配成功次数>5或者匹配次数超过40次就放回True直接退出循环
        if count > 5 or all_count > 40:
            return True
        return False  # 返回原始函数的返回值

    # 在闭包作用域内初始化计数器
    count = 0
    all_count = 0

    # 返回装饰后的函数，并附带计数器的引用
    return inner


def configure_ssh(self):
    if self.device_type in ["huawei", "h3c"]:
        self.client.send(CURRENT_CONFIG + ENTER)
        # pass


def save_configure(self):
    if self.device_type in ["huawei", "h3c"]:
        self.client.send("return".encode())
        self.client.send(HH_SAVE + ENTER)


@exit_count
def re_exit(msg: str, device_type: str = None) -> bool:
    if device_type in ["huawei", "h3c"]:
        r: list = re.findall(r">$|]$", msg)
        if r:
            return True
        else:
            return False
    else:
        return False


class Connect:

    def __init__(self, hostname: str, username: str, password: str, port: int = 22, device_type: str = None, **kwargs):
        self.hostname: str = hostname
        self.username: str = username
        self.password: str = password
        self.device_type: str = device_type
        self.port: int = port
        self.result: Dict[str, Any] = {}
        self._update_att(**kwargs)
        self.client: Channel = None
        self.save = False

    def __enter__(self):
        _, self.client = self.connect()

    def __exit__(self, exc_type, exc_val, exc_tb):
        if self.client:
            self.client.close()

    def connect(self) -> tuple[bool, Channel]:
        def open_connect():
            b, self.client = self._open
            if not b:
                return b, self.result
            self._screen()
            return b, self.client

        return open_connect()

    def run_command(self, command: str | bytes | list, multiple: bool = False) -> str:
        """
        如果需要执行多条命令则需要按照以下格式传递，默认不会进入配置模式，请直接在脚本中显示的声明进入配置模式\n
#
interface Vlanif20
 ip address 172.16.1.1 255.255.255.0
 ospf network-type p2p
 ospf enable 1 area 0.0.0.0
#
    也可以将多个命令使用列表的形式传递,如果是已列表传递则不需要声明multiple
    ['interface Vlanif20','ip address 172.16.1.1 255.255.255.0', 'ospf network-type p2p','ospf enable 1 area 0.0.0.0']
    也可以将多个命令直接传递，multiple可以不用传，默认是会自动回车
        :param multiple: 是否是多个命令
        :param command: 运行的命令
        :return: 运行命令的返回值
        """
        msg: str = ""
        if isinstance(command, list):
            for i in command:
                self.client.send(i.encode())
                self.client.send(ENTER)
        else:
            if multiple:
                if not isinstance(command, str):
                    raise ValueError("命令格式不对！")
                for i in command.split('\n'):
                    self.client.send(i.encode())
                    self.client.send(ENTER)
            else:
                self.client.send(command.encode())
                self.client.send(ENTER)
        # time.sleep(1)
        while True:
            temp = self.client.recv(65535).decode()
            self.client.send(ENTER)
            time.sleep(0.5)
            msg += temp
            if re_exit(msg=temp, device_type=self.device_type):
                self.client.close()
                break
        print(msg)
        self.result = self._handle_result(data=msg)
        return msg

    def _disable_screen(self):
        match self.device_type:
            case None:
                self.client.close()
                raise Exception("设备类型不能为空")
            case "huawei":
                self.client.send(HUAWEI_SCREEN + ENTER)
            case "h3c":
                self.client.send(H3C_SCREEN + ENTER)

    def _screen(self) -> None:
        self._disable_screen()
        time.sleep(0.5)

    @property
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
            return True, self.client.invoke_shell()
        except AuthenticationException as au:
            self.result = self._handle_result(code=False, msg="账号密码错误")
            return False, None
        except ChannelException as ce:
            self.result = self._handle_result(code=False, msg="通道异常")
            return False, None
        except TimeoutError as te:
            self.result = self._handle_result(code=False, msg="连接超时")
            return False, None
        except IOError as ioe:
            self.result = self._handle_result(code=False, msg="连接异常！")
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

    @property
    def get_configure(self) -> dict:
        t, c = self.connect()
        if not t:
            return self._handle_result(code=False, msg="error", data=c)
        config: str = self.run_command(command=CURRENT_CONFIG)
        self.result: dict = self._handle_result(data=config)
        return self.result

    def _update_att(self, **kwargs) -> None:
        """
        动态的添加类属性，防止程序报错
        :param kwargs:
        :return:
        """
        for k, v in kwargs.items():
            self.__setattr__(k, v)


if __name__ == '__main__':
    d: list = [
        dict(hostname='10.10.10.2', username='admin', password='qxxx1473464511mm', port=22, device_type="h3c"),
        dict(hostname='10.10.10.1', username='admin', password='qxxx1473464511mm', port=22, device_type="huawei"),
    ]
    # c = Connect(hostname='10.10.10.1', username='admin', password='qxxx1473464511mm', port=22, comm="1232423",
    #             version="v2c", oid="0.0.0.1.0.101", device_type="huawei")
    # print(c.__dict__)
    # result = c.get_configure
    # print(c.__dict__)
    # c.run_command()
    # _ = c.get_configure
    # c.connect()
    # c.run_command(m)
    # print(c.get_configure)
    for i in d:
        c = Connect(**i)
        c.connect()
        c.run_command(CURRENT_CONFIG)
        print(c.result)
        # print(Connect(**i).get_configure)
