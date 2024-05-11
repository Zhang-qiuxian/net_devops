DATABASES = {
    'default': {
        'ENGINE': 'django.db.backends.postgresql',
        'NAME': 'net_devops',
        'USER': 'zhangqiuxian',
        'PASSWORD': 'Admin@1234',
        'HOST': '127.0.0.1',
        'PORT': '5432',
        # 'CONN_MAX_AGE': 500,
        # 2. 关于连接池的配置
        'POOL_OPTIONS': {
            'POOL_SIZE': 10,
            'MAX_OVERFLOW': 10
        }
    }
}
