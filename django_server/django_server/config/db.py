from pathlib import Path

BASE_DIR = Path(__file__).resolve().parent.parent.parent

# DATABASES = {
#     'default': {
#         'ENGINE': 'dj_db_conn_pool.backends.postgresql',
#         'NAME': 'net_devops',
#         'USER': 'zhangqiuxian',
#         'PASSWORD': 'Admin@1234',
#         'HOST': '127.0.0.1',
#         'PORT': '5432',
#         # 'CONN_MAX_AGE': 500,
#         # 2. 关于连接池的配置
#         'POOL_OPTIONS': {
#             'POOL_SIZE': 10,
#             'MAX_OVERFLOW': 10
#         }
#     }
# }

DATABASES = {
    'default': {
        'ENGINE': 'django.db.backends.sqlite3',
        'NAME': BASE_DIR / 'db.sqlite3',
    }
}

if __name__ == '__main__':
    print(BASE_DIR)
    print(__file__)
