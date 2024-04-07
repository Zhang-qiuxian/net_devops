from pathlib import Path

LOGS_DIRS = Path(__file__).resolve().parent.parent.parent.joinpath("logs")

# 日志
# LOGS_DIRS = os.path.join(BASE_DIR, 'logs')
# LOGS_DIRS = BASE_DIR.joinpath("logs")
LOGS_DIRS.mkdir(parents=True, exist_ok=True)
LOGGING = {
    'version': 1,  # 使用的日志模块的版本，目前官方提供的只有版本1，但是官方有可能会升级，为了避免升级出现的版本问题，所以这里固定为1
    'disable_existing_loggers': False,  # 是否禁用其他的已经存在的日志功能？肯定不能，有可能有些第三方模块在调用，所以禁用了以后，第三方模块无法捕获自身出现的异常了。
    'formatters': {  # 日志格式设置，verbose或者simple都是自定义的
        'verbose': {  # 详细格式，适合用于开发人员不在场的情况下的日志记录。
            # 格式定义：https://docs.python.org/3/library/logging.html#logrecord-attributes
            # levelname 日志等级
            # asctime   发生时间
            # module    文件名
            # process   进程ID
            # thread    线程ID
            # message   异常信息
            'format': '{levelname} {asctime} {module} {process:d} {thread:d} {message}',
            'style': '{',  # 变量格式分隔符
        },
        'simple': {  # 简单格式，适合用于开发人员在场的情况下的终端输出
            'format': '{levelname} {message}',
            'style': '{',
        },
        'api_log': {  # 简单格式，适合用于开发人员在场的情况下的终端输出
            'format': '{levelname} {asctime} {message}',
            'style': '{',
        },
    },
    'filters': {  # 过滤器
        'require_debug_true': {
            '()': 'django.utils.log.RequireDebugTrue',
        },
    },
    'handlers': {  # 日志处理流程，console或者mail_admins都是自定义的。
        'console': {
            'level': 'DEBUG',  # 设置当前日志处理流程中的日志最低等级
            'filters': ['require_debug_true'],  # 当前日志处理流程的日志过滤
            'class': 'logging.StreamHandler',  # 当前日志处理流程的核心类，StreamHandler可以帮我们把日志信息输出到终端下
            'formatter': 'simple'  # 当前日志处理流程的日志格式
        },
        # 'mail_admins': {
        #     'level': 'ERROR',                  # 设置当前日志处理流程中的日志最低等级
        #     'class': 'django.utils.log.AdminEmailHandler',  # AdminEmailHandler可以帮我们把日志信息输出到管理员邮箱中。
        #     'filters': ['special']             # 当前日志处理流程的日志过滤
        # }
        'file': {
            'level': 'INFO',
            'class': 'logging.handlers.TimedRotatingFileHandler',
            # 日志位置,日志文件名，日志保存目录logs必须手动创建
            'filename': '%s/django.log' % LOGS_DIRS,
            # TimedRotatingFileHandler的参数
            # 目前设定每天一个日志文件
            # 'S'         |  秒
            # 'M'         |  分
            # 'H'         |  时
            # 'D'         |  天
            # 'W0'-'W6'   |  周一至周日
            # 'midnight'  |  每天的凌晨
            'when': 'D',  # 间间隔的类型，指定秒就不要在Windows上运行测试
            'interval': 1,  # 时间间隔
            'backupCount': 30,  # 能留几个日志文件;过数量就会丢弃掉老的日志文件
            'encoding': 'utf-8',  # 日志文本编码
            'formatter': 'verbose'  # 当前日志处理流程的日志格式
        },
        'api': {
            'level': 'INFO',
            'filename': '%s/api.log' % LOGS_DIRS,
            'class': 'logging.handlers.RotatingFileHandler',
            'formatter': 'api_log',
            'maxBytes': 5 * 1024 * 1024,
            'backupCount': 10
        },
    },
    'loggers': {  # 日志处理的命名空间
        'django': {
            'handlers': ['console', 'file'],  # 当基于django命名空间写入日志时，调用那几个日志处理流程
            'propagate': True,  # 是否在django命名空间对应的日志处理流程结束以后，冒泡通知其他的日志功能。True表示允许
        },
        'api': {
            'handlers': ['api'],
            'level': 'INFO',
            'propagate': False,
        },
    }
}
