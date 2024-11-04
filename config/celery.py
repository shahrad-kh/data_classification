from __future__ import absolute_import, unicode_literals

import os

from celery import Celery
from celery.schedules import crontab
from django.conf import settings


# Set the default Django settings module
os.environ.setdefault('DJANGO_SETTINGS_MODULE', 'config.settings')

app = Celery('config')

# Load task modules from all registered Django app configs
app.config_from_object('django.conf:settings', namespace='CELERY')
app.autodiscover_tasks()

@app.task(bind=True)
def debug_task(self):
    print(f'Request: {self.request!r}')


# Define the Celery Beat Schedule
app.conf.beat_schedule = {
    'export-daily-logs': {
        'task': 'datasets.tasks.export_daily_logs',
        'schedule': crontab(hour=0, minute=0),  # Executes every day at 00:00
    },
}