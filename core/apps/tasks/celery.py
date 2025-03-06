from __future__ import absolute_import, unicode_literals

import os

from celery import Celery
from celery.schedules import crontab

os.environ.setdefault('DJANGO_SETTINGS_MODULE', 'core.config.django.base')

app = Celery('Universitly')

app.config_from_object('django.conf:settings', namespace='CELERY')

app.autodiscover_tasks()

app.conf.update(
    result_expires=3600,
    broker_connection_retry_on_startup=True,
)

app.conf.beat_schedule = {
    'send_weekly_emails': {
        'task': 'core.apps.tasks.tasks.send_weekly_emails',
        'schedule': crontab(day_of_week='FRI', hour='16'),
        'kwargs': {'email_type': 'M'},
    },
}
