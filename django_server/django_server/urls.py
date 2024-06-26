"""
URL configuration for django_server project.

The `urlpatterns` list routes URLs to views. For more information please see:
    https://docs.djangoproject.com/en/5.0/topics/http/urls/
Examples:
Function views
    1. Add an import:  from my_app import views
    2. Add a URL to urlpatterns:  path('', views.home, name='home')
Class-based views
    1. Add an import:  from other_app.views import Home
    2. Add a URL to urlpatterns:  path('', Home.as_view(), name='home')
Including another URLconf
    1. Import the include() function: from django.urls import include, path
    2. Add a URL to urlpatterns:  path('blog/', include('blog.urls'))
"""
from django.contrib import admin
from django.urls import path, include, re_path
from django.views.static import serve
from django.conf import settings

from rest_framework.response import Response
from rest_framework.views import APIView
from rest_framework.request import Request

from drf_yasg.views import get_schema_view
from drf_yasg import openapi

from apps.device.models import Device
from .urls_api import router, api_url


class TestApiView(APIView):
    def get(self, request):
        return Response({"code": 200, "message": "ok"})


class PingApiView(APIView):
    def get(self, request: Request):
        """
        测试接口
        :param request:
        :return:
        """
        return Response({"code": 200, "message": "ok"})


schema_view = get_schema_view(
    openapi.Info(
        title="net_devops API",
        default_version='v1',
        description="net_devops 后台api接口",
        # terms_of_service="https://www.google.com/policies/terms/",
        contact=openapi.Contact(name='联系邮箱', email="1473464511@qq.com"),
        license=openapi.License(name="BSD License"),
    ),
    public=True,
    # permission_classes=(permissions.AllowAny,),
)

urlpatterns = [
    # path('admin/', admin.site.urls),
    path('api/ping', PingApiView.as_view(), name='ping'),
    path('api/test', TestApiView.as_view(), name='test'),
    path('api/v1/', include(router.urls), name='api-v1'),
    path('api/swagger<format>/', schema_view.without_ui(cache_timeout=0), name='schema-json'),
    path('api/swagger/', schema_view.with_ui('swagger', cache_timeout=0), name='schema-swagger-ui'),
    path('api/redoc/', schema_view.with_ui('redoc', cache_timeout=0), name='schema-redoc'),
    re_path(r"^media/(?P<path>.*)$", serve, {'document_root': settings.MEDIA_ROOT}, name='media'),

]
urlpatterns += api_url
