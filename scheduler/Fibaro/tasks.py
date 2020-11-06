import base64
import json
import logging
from datetime import datetime

from celery import Celery
from django.core import serializers
from django.db.models import Max

from fibaro.adapter import HomeCenterAdapter
import fibaro.models
from fibaro.ypostirizo import Cloud
from ypostirizoclient import settings

app = Celery('tasks', broker='redis://localhost:6379//')


@app.task
def get_sensor_data():
    """
    Async tasks that fetches (on a scheduled basis) data regarding
    the Fibaro sensors via Home Center lite's API endpoint.
    """
    home_center_adapter = HomeCenterAdapter()

    devices = home_center_adapter.get(endpoint='/api/devices', method='GET').json()
    for d in devices:
        device = fibaro.models.Device()
        device.read_json(d)
        device.save()


@app.task
def get_events():
    """
    Async tasks that fetches (on a scheduled basis) data regarding
    the Events that were registered on the Home Center Lite via
    the hub's API endpoint.
    """
    home_center_adapter = HomeCenterAdapter()
    parameters = {}
    event_max_time = fibaro.models.EventBase.objects.all().aggregate(Max('timestamp')).get('timestamp__max')
    parameters['from'] = event_max_time

    new_events = home_center_adapter.get(endpoint='/api/panels/event',
                                         parameters=parameters,
                                         method='GET').json()

    for new in new_events:
        event = fibaro.models.EventBase()
        if new is not None:
            event.read_json(new)
            event.save()
