import time

from django.utils.deprecation import MiddlewareMixin
from django.http import HttpRequest
from rest_framework.request import Request
from rest_framework.response import Response
from typing import Any

from utils.logger import api_logger


def _get_host(meta: dict[str, str]) -> str:
    """
    处理客户端的ip地址
    :param meta:请求头字典
    :return:客户端ip
    """
    # 常见的客户端ip字典
    host_str: list[str] = ['x-forwarded-for', 'proxy-client-ip', 'wl-proxy-client-ip',
                           'http_client_ip', 'x-real-ip', 'remote_addr']
    for k, v in meta.items():
        if k.lower() in host_str:
            if v not in ",":
                return v
            return v.split(",")[0]


# def _handle_header(headers: dict[str, str]):
#     # 脱密
#     exclude_key: list[str] = ['password', 'token', 'access', 'refresh']
#     header: dict[str, str] = {}
#     for k, v in headers.items():
#         if k.lower() not in exclude_key:
#             header[k.lower()] = v
#         else:
#             header[k.lower()] = "*" * 8
#     return header


def _handle_request_message(request: HttpRequest) -> dict[str, str]:
    """
    获取请求头中的信息,将大写的key全部转为小写
    :param request:请求信息
    :return:获取的字典
    """

    headers: dict[str, str] = {k.lower(): v for k, v in request.headers.items()}
    headers["host"] = _get_host(request.META)
    headers["path"] = request.path
    headers["method"] = request.method
    headers["protocol"] = request.META.get("SERVER_PROTOCOL")
    return headers


# 跨域中间件
class ApiLogMiddleware(MiddlewareMixin):
    """ 记录 api 请求日志 """

    def process_request(self, request: HttpRequest):
        """ 在这里处理 request 请求 """
        request.before_time = time.perf_counter()
        setattr(request, "request_info", _handle_request_message(request))

    def process_response(self, request: Request, response: Response) -> Response:
        """ 记录返回 response 记录日志 """
        before_time: float = request.before_time
        count_time: str = f"{round((time.perf_counter() - before_time) * 1000, 3)} ms"
        request_info: dict[str, str] = request.request_info
        request_info["time"] = count_time
        api_logger.info(msg=request_info)
        return response
