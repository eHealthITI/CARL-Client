import base64
import json
import logging
from datetime import datetime

from celery import Celery
from django.core import serializers
from django.db.models import Max

from fibaro.adapter import HomeCenterAdapter
from fibaro.models import Section, Device, EventBase, Room
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
        device = Device()
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
    event_max_time = EventBase.objects.all().aggregate(Max('timestamp')).get('timestamp__max')
    parameters['from'] = event_max_time

    new_events = home_center_adapter.get(endpoint='/api/panels/event',
                                         parameters=parameters,
                                         method='GET').json()

    for new in new_events:
        event = EventBase()
        if new is not None:
            event.read_json(new)
            event.save()


@app.task
def get_sections():
    """
    Async tasks that fetches (on a scheduled basis) data regarding
    the Scenes that were registered on the Home Center Lite via
    the hub's API endpoint.
    """
    home_center_adapter = HomeCenterAdapter()

    new_sections = home_center_adapter.get(endpoint='/api/sections',
                                           method='GET').json()

    for new in new_sections:
        section = Section()
        if new is not None and Section.objects.get(pk=new['id']) is None:
            section.read_json(new)
            section.save()


@app.task
def get_rooms():
    """
    Async tasks that fetches (on a scheduled basis) data regarding
    the Rooms that were registered on the Home Center Lite via
    the hub's API endpoint.
    """
    home_center_adapter = HomeCenterAdapter()

    new_rooms = home_center_adapter.get(endpoint='/api/rooms',
                                        method='GET').json()

    for new in new_rooms:
        section = Section()
        if new is not None and Room.objects.get(pk=new['id']) is None:
            section.read_json(new)
            section.save()
