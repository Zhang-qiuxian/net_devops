import time
from ipaddress import IPv4Network, IPv6Network, ip_network, ip_address, IPv4Address, ip_interface
from rest_framework.exceptions import APIException


# import os
# import django
#
# os.environ.setdefault('DJANGO_SETTINGS_MODULE', 'server.settings')
# django.setup()

# 校验sub是否在master的网段里面
def check_subnet_of(master: str, sub: str) -> bool:
    m = ip_network(master)
    s = ip_network(sub)
    if s.subnet_of(m):
        return True
    else:
        return False


# 校验master是否在super的网段里面
def check_supernet_of(master: str, sub: str) -> bool:
    m = ip_network(master)
    s = ip_network(sub)
    if m.supernet_of(s):
        return True
    else:
        return False


# 校验两个网络号是否相同
def check_master_eq_sub_net(master_net: str, sub_net: str):
    if master_net == sub_net:
        return True
    else:
        return False


# 校验ip地址是否正确，返回ip地址对象
def check_net(network: str, mask: int | str) -> IPv4Network | IPv6Network:
    try:
        ip = ip_network(f"{network}/{mask}", strict=False)
        return ip
    except ValueError as v:
        raise APIException(code=1000, detail="ip地址解析失败！")


# 校验前端传过来的掩码是符合规范,主网络号
def _check_master_mask(mask: int):
    if mask in [31, 32, 127, 128] or mask < 8 or mask > 128:
        raise APIException(code=1000, detail="请确认掩码！")
    else:
        return True


# 校验并处理前端传递过来的ip
def check_master_network(network: str, mask: int) -> str:
    if _check_master_mask(mask):
        ip = check_net(network=network, mask=mask)
        net = ip.network_address
        return net.__str__()


# 根据ip和掩码生成这一段的所有主机ip
def generate_host_ip(net: str, mask: int) -> list[str]:
    ip = check_net(network=net, mask=mask)
    network: list = [addr.__str__() for addr in ip.hosts()]
    return network


# 根据ip和掩码生成这一段的所有主机ip
def generate_all_ip(net: str, mask: int) -> list[str]:
    ip = check_net(network=net, mask=mask)
    network: list = [addr.__str__() for addr in ip]
    return network


def check_num_addr(network: str, mask: int) -> int:
    ip = check_net(network, mask)
    return ip.num_addresses


# 校验ip是否属于网段内
def check_ip_in_net(addr: str, net: str, net_mask: int) -> bool:
    ip = ip_address(addr)
    network = check_net(net, net_mask)
    if ip in network:
        return True
    else:
        return False


if __name__ == '__main__':
    # _, net = check_net(network="192.168.0.1", mask=24)
    # print(generate_all_ip("192.168.0.1", 24))
    m = "192.168.0.0/24"
    # s = "192.168.0.128/25"
    # print(check_supernet_of(m, s))
    start = time.time()
    check_ip_in_net("192.168.10.254", "192.168.1.1", 20)
    # m1 = check_net("192.168.0.5", "255.255.255.0")
    m1 = check_net("192.168.0.5", 24)
    print(m1.hosts())
    print(m1.num_addresses)
    print(m1.subnets())
    print(m1.max_prefixlen)
    print(m1.with_hostmask)
    print(m1.reverse_pointer)
    print(m1.network_address.exploded,type(m1.network_address.exploded))
    print(m1.netmask.exploded)
    print(m1.prefixlen)
    # print(m1.hosts())
    # print(m1.hosts())
