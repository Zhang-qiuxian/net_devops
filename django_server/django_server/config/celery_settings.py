from django.conf import settings

from celery.schedules import crontab
from datetime import timedelta

# Celery Configuration Options
CELERY_TASK_TRACK_STARTED = True
# Broker配置，使用Redis作为消息中间件
# BROKER_URL = 'redis://127.0.0.1:6379/0'


# 任务结果过期时间，秒
CELERY_TASK_RESULT_EXPIRES = 60 * 60 * 24
# 最重要的配置，设置消息broker,格式为：db://user:password@host:port/dbname
# 如果redis安装在本机，使用localhost
# 如果docker部署的redis，使用redis://redis:6379
CELERY_BROKER_URL = "redis://127.0.0.1:6379/0"  # 消息中间件（Broker）使用 redis 数据库。
# 时区配置
CELERY_TIMEZONE = settings.TIME_ZONE
CELERY_ENABLE_UTC = False
DJANGO_CELERY_BEAT_TZ_AWARE = False

# 为 django_celery_results 存储 Celery 任务执行结果设置后台
# 格式为：格式为：db+scheme://user:password@host:port/dbname
# 支持数据库 django-db 和缓存 django-cache 存储任务状态及结果
CELERY_RESULT_BACKEND = "django-db"  # Celery 任务执行结果保存到 django数据库中

# celery内容等消息的格式设置，默认json
CELERY_ACCEPT_CONTENT = ['json', 'pickle']
CELERY_TASK_SERIALIZER = 'pickle'
CELERY_RESULT_SERIALIZER = 'pickle'

# 为任务设置超时时间，单位秒。超时即中止，执行下个任务。
CELERY_TASK_TIME_LIMIT = 500
# Celery Beat 配置
CELERY_BEAT_SCHEDULER = 'django_celery_beat.schedulers.DatabaseScheduler'

# 配置定时任务


CELERY_BEAT_SCHEDULE = {
    '同步设备基本信息': {
        'task': 'apps.device.tasks.start_sync',  # 任务
        'schedule': timedelta(minutes=1),  # 每1分钟执行函数
        # 'args': ()  # 运行参数
    },
    '同步arp信息': {
        'task': 'apps.device.tasks.start_sync_arp',  # 任务
        'schedule': timedelta(minutes=20),  # 每20分钟执行函数
        # 'args': ()  # 运行参数
    },

}
