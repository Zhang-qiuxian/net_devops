# **跨域配置**
# CORS_ORIGIN_ALLOW_ALL为True, 指定所有域名(ip)都可以访问后端接口, 默认为False
CORS_ORIGIN_ALLOW_ALL = True
CORS_ALLOW_ALL_ORIGINS = True
CORS_ALLOW_CREDENTIALS = True # 会话保持必须

# 非必须
# CORS_ALLOW_METHODS = (
#     "GET",
#     "POST",
#     "PUT",
#     "DELETE",
#     'OPTIONS'
#     'PATCH',
#     'VIEW'
# )

# 非必须
CORS_ALLOW_HEADERS = (
    "XMLHttpRequest",
    'token',
    'X_FILENAME',
    'accept',
    'accept-encoding',
    'authorization',
    'content-type',
    'dnt',
    'origin',
    'user-agent',
    'x-csrftoken',
    'x-requested-with',
)
# 暴露响应头，xhr才可以拿到响应头
CORS_EXPOSE_HEADERS = ('token',)
# 缓存options请求
CORS_PREFLIGHT_MAX_AGE = 86400  # 秒