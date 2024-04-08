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
from django.urls import path, include

from rest_framework.response import Response
from rest_framework.views import APIView
from rest_framework.request import Request

from .urls_api import router, api_url


class PingApiView(APIView):
    def get(self, request: Request):
        return Response({"code": 200, "message": "ok"})


urlpatterns = [
    # path('admin/', admin.site.urls),
    path('ping', PingApiView.as_view(), name='ping'),
    path('api/v1/', include(router.urls), name='api-v1'),
]
urlpatterns += api_url
