from __future__ import absolute_import, unicode_literals
from celery import Celery
import os

from celery.schedules import crontab

from ypostirizoclient import settings

os.environ.setdefault('DJANGO_SETTINGS_MODULE', 'ypostirizoclient.settings')

app = Celery('scheduler',
             broker='redis://redis:6379',
             include=['scheduler.Cloud.tasks',
                      #'scheduler.Fibaro.tasks'
                    ])

app.config_from_object('scheduler.celeryconfig')

app.conf.beat_schedule = {
    'check-for-new-sections': {
        'task': 'scheduler.Fibaro.tasks.get_sections',
        'schedule': 5
    },
    'check-for-new-rooms': {
        'task': 'scheduler.Fibaro.tasks.get_rooms',
        'schedule':5  
    },
    'check-for-new-events': {
        'task': 'scheduler.Fibaro.tasks.get_events',
        'schedule': 5
    },
    'check-for-new-devices': {
        'task': 'scheduler.Fibaro.tasks.get_sensor_data',
        'schedule': 10
    },
    'push-new-sections': {
        'task': 'scheduler.Cloud.tasks.upload_sections',
        'schedule': 60  # seconds
    },
    'push-new-rooms': {
        'task': 'scheduler.Cloud.tasks.upload_rooms',
        'schedule': 60  # seconds
    },
    'push-new-devices': {
        'task': 'scheduler.Cloud.tasks.update_devices',
        'schedule': 10  # seconds
    },
    'push-latest-events': {
        'task': 'scheduler.Cloud.tasks.upload_events',
        'schedule': 10 # seconds
    }

}

if __name__ == '__main__':
    app.start()
