import base64
import json
import logging
import time
from datetime import datetime

import django
from celery import Celery
from django.core import serializers
from django.core.exceptions import ObjectDoesNotExist
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
    for device in devices:
        try:
            sensor = fibaro.models.Device()
            sensor.read_json(device)
            sensor.save()

        # TODO Probably should remove this exception
        except ObjectDoesNotExist:
            logging.info('the roomId is : {}'.format(device.get('roomID')))
            logging.info('the parentId is : {}'.format(device.get('parentId')))


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
    if event_max_time is None:
        parameters['from'] = 0
    else:
        parameters['from'] = event_max_time

    endpoint = '/api/panels/event'

    response = home_center_adapter.get(endpoint=endpoint,
                                       parameters=parameters,
                                       method='GET')

    new_events = response.json()
    for new in new_events:
        if new is not None:
            event = fibaro.models.EventBase()
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
        section = fibaro.models.Section()
        if new is not None:
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
        room = fibaro.models.Room()
        if new is not None:
            room.read_json(new)
            room.save()
