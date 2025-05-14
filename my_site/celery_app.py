import os
import time
import celery
from celery.schedules import crontab

from django.conf import settings

os.environ.setdefault('DJANGO_SETTINGS_MODULE', 'my_site.settings')

app = celery.Celery('core')
app.config_from_object('django.conf:settings')
app.conf.broker_url = 'redis://redis:6379/0'
app.autodiscover_tasks()
