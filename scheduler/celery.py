from __future__ import absolute_import, unicode_literals
from celery import Celery
import os

from ypostirizoclient import settings

os.environ.setdefault('DJANGO_SETTINGS_MODULE', 'ypostirizoclient.settings')

app = Celery('scheduler',
             broker='redis://localhost:6379',
             include=['scheduler.tasks'])
app.config_from_object('scheduler.celeryconfig')

app.conf.beat_schedule = {
    'check-for-new-events': {
        'task': 'scheduler.tasks.get_events_from_fibaro',
        'schedule': settings.HC_API_EVENT_INTERVAL
    },
    'push-latest-events': {
        'task': 'scheduler.tasks.send_to_cloud',
        'schedule': settings.DB_EVENT_INTERVAL
    }
}

if __name__ == '__main__':
    app.start()
