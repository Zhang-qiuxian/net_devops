# **rest_framework配置**
REST_FRAMEWORK = {
    "UNAUTHENTICATED_USER": None,
    "UNAUTHENTICATED_TOKEN": None,
    # 认证组件
    "DEFAULT_AUTHENTICATION_CLASSES": [
        # "public.auth_middleware.JwtHeaderAuthentication",
        # "public.auth_middleware.NoAuthentication"
    ],

    # 权限组件
    'DEFAULT_PERMISSION_CLASSES': [
    ],
    # 分页器组件
    'DEFAULT_PAGINATION_CLASS': 'public.paginator.CommentPagination',
    'PAGE_SIZE': 10,
    # 自定义异常处理
    "EXCEPTION_HANDLER": "public.exceptions.exception_handler",
    "DATE_FORMAT": "%Y-%m-%d",
    "DATETIME_FORMAT": "%Y-%m-%d %H:%M:%S",
    # 过滤器默认后端
    'DEFAULT_FILTER_BACKENDS': [
        'rest_framework.filters.OrderingFilter',
        'rest_framework.filters.SearchFilter',
        'django_filters.rest_framework.DjangoFilterBackend',
    ],
    # 接口文档
    'DEFAULT_SCHEMA_CLASS': 'rest_framework.schemas.coreapi.AutoSchema',
}
