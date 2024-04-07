import logging.config
from logging import Logger
from django.conf import settings

django_logger: Logger = logging.getLogger('django')
api_logger: Logger = logging.getLogger("api")
# logging.config.dictConfig(settings.LOGGING)  # logging配置
