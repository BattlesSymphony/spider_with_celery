# coding=utf-8
import os
from celery import Celery
# celery 里面有一些定时任务 可以同crontab 添加到task上
from celery.schedules import crontab
from kombu import Queue
from django.conf import settings

os.environ.setdefault('DJANGO_SETTINGS_MODULE', 'wechat.settings')

# 创建app
app = Celery('top250')
# 从django项目中读取信息
app.config_from_object('django.conf:settings', namespace='CELERY')
# 自动寻找tasks
app.autodiscover_tasks()
# 默认队列名字叫 default
app.conf.task_default_queue = 'default'
app.conf.timezone = 'Asia/Shanghai'