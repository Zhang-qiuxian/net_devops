from typing import Any

from rest_framework.response import Response


class ResponseOK(Response):
    def __init__(self, data: Any = None, message: str = "success"):
        res = dict(code=200, status="success", message=message, data=data)
        super().__init__(data=res)


class ResponseError(Response):
    def __init__(self, data: Any = None, code: int = 400, message: str = "fault"):
        res = dict(code=code, status="error", message=message, data=data)
        super().__init__(data=res)


class ResponseInfo(Response):
    def __init__(self, data: Any = None, code: int = 1000, message: str = "warning"):
        res = dict(code=code, status="warning", message=message, data=data)
        super().__init__(data=res)
