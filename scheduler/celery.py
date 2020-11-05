from __future__ import absolute_import, unicode_literals
from celery import Celery
import os

from ypostirizoclient import settings

os.environ.setdefault('DJANGO_SETTINGS_MODULE', 'ypostirizoclient.settings')

app = Celery('scheduler',
             broker='redis://localhost:6379',
             include=['scheduler.Cloud.tasks',
                      'scheduler.Fibaro.tasks'])

app.config_from_object('scheduler.celeryconfig')

app.conf.beat_schedule = {
    'check-for-new-events': {
        'task': 'scheduler.Fibaro.tasks.get_events',
        'schedule': settings.HC_API_EVENT_INTERVAL
    },
    'check-for-new-devices': {
        'task': 'scheduler.Fibaro.tasks.get_sensor_data',
        'schedule': settings.HC_API_EVENT_INTERVAL
    },
    'push-latest-events': {
        'task': 'scheduler.Cloud.tasks.upload_events',
        'schedule': 30   # seconds
    },
    'push-new-devices': {
        'task': 'scheduler.Cloud.tasks.update_devices',
        'schedule': 15  # seconds
    }

}

if __name__ == '__main__':
    app.start()
