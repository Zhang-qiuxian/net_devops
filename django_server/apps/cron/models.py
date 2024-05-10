from django.db import models


# Create your models here.

class CronJobSyncLog(models.Model):
    job = models.CharField(max_length=32, verbose_name="任务名称", db_comment="任务名称")
    status = models.CharField(max_length=32, default="success", verbose_name="任务完成状态", db_comment="任务完成状态")
    data = models.JSONField(verbose_name="任务详情", db_comment="任务详情")
    create_time = models.DateTimeField(auto_now_add=True, verbose_name="创建时间", db_comment="创建时间")

    def __str__(self):
        return self.job

    class Meta:
        db_table = 'cron_job_sync_log'
        verbose_name = '定时任务同步日志'
        verbose_name_plural = verbose_name
        db_table_comment = '定时任务同步日志'
        ordering = ['-id']
