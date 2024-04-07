import http

from rest_framework.pagination import PageNumberPagination
from rest_framework.response import Response
from collections import OrderedDict

from public.response import ResponseOK


# class IPPagination(PageNumberPagination):
#     page_size = 256
#     page_size_query_param = "page_size"
#
#     def get_paginated_response(self, data) -> Response:
#         data: dict = dict(total=self.page.paginator.count, data=data)
#         return Ok(message="ok", data=data)


class CommentPagination(PageNumberPagination):
    max_page_size = 100
    page_size_query_param = "page_size"

    def get_paginated_response(self, data) -> Response:
        data: dict = dict(total=self.page.paginator.count, data=data)
        return ResponseOK(message="ok", data=data)
