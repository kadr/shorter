from __future__ import absolute_import, unicode_literals

import os

from celery import Celery
from celery.schedules import crontab

os.environ.setdefault('DJANGO_SETTINGS_MODULE', 'short_urls.settings')

app = Celery('short_urls')

app.config_from_object('django.conf:settings', namespace='CELERY')


app.autodiscover_tasks()

app.conf.beat_schedule = {
    'run-every-single-minute': {
        'task': 'short_urls.Url.tasks.remove_old_url_starter',
        'schedule': crontab(minute=0, hour=0, day_of_week='monday'),
    },
}


