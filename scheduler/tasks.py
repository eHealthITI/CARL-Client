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
def get_events_from_fibaro():
    parameters = {}
    home_center_adapter = HomeCenterAdapter()
    event_max_time = fibaro.models.EventBase.objects.all().aggregate(Max('timestamp')).get('timestamp__max')
    parameters['from'] = event_max_time

    new_events = home_center_adapter.get(endpoint='/api/panels/event', parameters=parameters, method='GET').json()
    for new in new_events:
        event = fibaro.models.EventBase()
        if new is not None:
            event.read_json(new)
            event.save()


@app.task
def get_events_from_local_db():

    events = fibaro.EventBase().objects.filter()


@app.task
def find_devices():
    logging.info("Initiating search for devices.")
    home_center_adapter = HomeCenterAdapter()
    # Using HomeCenterAdapter to access the API
    devices = home_center_adapter.get().json()
    for d in devices:
        if d['type'] not in settings.IGNORED_DEVICES:
            device = fibaro.models.Device()
            device.read_json(d)
            device.save()


@app.task
def send_to_cloud():
    # this task is going to be used to send the data to the cloud
    current_time = int(datetime.now().timestamp())
    latest_events = fibaro.models.EventBase.objects.filter(timestamp__gte=current_time-settings.DB_EVENT_INTERVAL)
    cloud = Cloud()
    event_json = serializers.serialize('json', latest_events)
    if event_json:
        cloud.send(endpoint='/api/device/events/new_event/',
                   payload=event_json)


@app.task
def send_to_radar_base():
    #this task is going to be used to send the data to the cloud
    pass
