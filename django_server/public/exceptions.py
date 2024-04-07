import http

from django.db import connections
from django.http import Http404
from django.conf import settings

from rest_framework import exceptions
from rest_framework.response import Response

from typing import Union
from public.status_code import API_ERROR


def set_rollback():
    for db in connections.all():
        if db.settings_dict['ATOMIC_REQUESTS'] and db.in_atomic_block:
            db.set_rollback(True)


def exception_handler(exc, context):
    """
    Returns the response that should be used for any given exception.

    By default we handle the REST framework `APIException`, and also
    Django's built-in `Http404` and `PermissionDenied` exceptions.

    Any unhandled exceptions may return `None`, which will cause a 500 error
    to be raised.
    """
    if isinstance(exc, Http404):
        exc = exceptions.NotFound()
    elif isinstance(exc, exceptions.PermissionDenied):
        exc = exceptions.PermissionDenied()

    if isinstance(exc, exceptions.APIException):
        headers = {}
        data: Union[dict | list] = {}
        if getattr(exc, 'auth_header', None):
            headers['WWW-Authenticate'] = exc.auth_header
        if getattr(exc, 'wait', None):
            headers['Retry-After'] = '%d' % exc.wait

        if isinstance(exc.detail, (list, dict)):
            data = exc.detail
        elif isinstance(exc.detail, exceptions.ErrorDetail):
            data: dict = {"code": API_ERROR, "status": "error", 'message': exc.detail}
        set_rollback()
        return Response(data, status=exc.status_code, headers=headers)
    # elif isinstance(exc, Exception):
    #     if not settings.DEBUG:
    #         return Response(status=500, data="服务器内部错误！")
    return None
