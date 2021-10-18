import base64
import json
import logging
import time
import celery
from datetime import datetime

import django
from celery import Celery
from django.core import serializers
from django.core.exceptions import ObjectDoesNotExist
from django.db.models import Max
from celery.utils.log import get_task_logger

from fibaro.adapter import HomeCenterAdapter
import fibaro.models
from fibaro.ypostirizo import Cloud
from ypostirizoclient import settings

app = Celery('tasks', broker='redis://localhost:6379//')
from celery.utils.log import get_task_logger
import logging
Log_Format = "%(levelname)s %(asctime)s - %(message)s"
logging.basicConfig(filename = "logfile.log",
                    filemode = "w",
                    format = Log_Format, 
                    level = logging.ERROR)
logger = logging.getLogger()
logger.error("Our First Log Message")



@app.task
def get_sensor_data():
    """
    Async tasks that fetches (on a scheduled basis) data regarding
    the Fibaro sensors via Home Center lite's API endpoint.
    """
    logger = logging.getLogger()
    home_center_adapter = HomeCenterAdapter()
    devices = home_center_adapter.get(endpoint='/api/devices', method='GET')
    if devices is not None:    
        for device in devices.json():
            try:
                sensor = fibaro.models.Device()
                sensor.read_json(device)
                sensor.save()
                logger.info(f'_________________GET SENSOR DATA _____________ ')
                logger.info(f' Device JSON #######: \n{device} ')
                logger.info(f' Device Object #######: \n {sensor.__dict__} ')
                logger.info(f'______________________________________________ ')
            # TODO Probably should remove this exception
            except ObjectDoesNotExist:
                logger.info('the roomId is : {}'.format(device.get('roomID')))
                logger.info('the parentId is : {}'.format(device.get('parentId')))


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

    new_events = home_center_adapter.get(endpoint=endpoint,
                                       parameters=parameters,
                                       method='GET')

    if new_events is not None:
        for new in new_events.json():
            if new is not None:
                event = fibaro.models.EventBase()
                event.read_json(new)
                event.save()
                logger.debug(f'_________________GET EVENTS _____________ ')
                logger.debug(f' Event JSON #######: \n{new} ')
                logger.debug(f' Event Object #######: \n {event.__dict__} ')
                logger.debug(f'______________________________________________ ')


@app.task
def get_sections():
    """
    Async tasks that fetches (on a scheduled basis) data regarding
    the Scenes that were registered on the Home Center Lite via
    the hub's API endpoint.
    """
    logger.debug(f'_________________GET SECTIONS _____________ ')
    home_center_adapter = HomeCenterAdapter()

    new_sections = home_center_adapter.get(endpoint='/api/sections',
                                           method='GET')
    if new_sections is  not None:
        for new in new_sections.json():
            section = fibaro.models.Section()
            if new is not None:
                section.read_json(new)
                section.save()

                logger.debug(f' Section JSON #######: \n{new} ')
                logger.debug(f' Section Object #######: \n {section.__dict__} ')
    logger.debug(f'______________________________________________ ')


@app.task
def get_rooms():
    """
    Async tasks that fetches (on a scheduled basis) data regarding
    the Rooms that were registered on the Home Center Lite via
    the hub's API endpoint.
    """
    logger.debug(f'_________________GET ROOMS _____________ ')
    home_center_adapter = HomeCenterAdapter()

    new_rooms = home_center_adapter.get(endpoint='/api/rooms',
                                        method='GET')
    if new_rooms is not None:
        for new in new_rooms.json():
            room = fibaro.models.Room()
            if new is not None:
                room.read_json(new)
                room.save()

                logger.debug(f' Room JSON #######: \n{new} ')
                logger.debug(f' Room Object #######: \n {room.__dict__} ')
    logger.debug(f'______________________________________________ ')
                
@app.task
def get_consumption():
    logger.debug(f'_________________GET CONSUMPTIONS _____________ ')
    devices = fibaro.models.Device.objects.filter(type='com.fibaro.FGWP102')
    home_center_adapter = HomeCenterAdapter()
    
    for device in devices:    
        last_consumption = fibaro.models.Consumption.objects.filter(device=device).order_by('timestamp').last()
        if last_consumption:
            last_timestamp = last_consumption.timestamp
        else:
            last_timestamp = 1622537945
        logger.debug(f' last timestmamp #######: \n{last_timestamp} ')
        
        endpoint = f'/api/energy/{last_timestamp}/now/summary-graph/devices/power/{device.id}'
        
        consumption_metrics = home_center_adapter.get(endpoint=endpoint,
                                                    method='GET')
        logger.debug(f' consumption_metrics raw #######: \n{consumption_metrics} ')
        
        cons_json = consumption_metrics.content.decode('utf8').replace("'", '"')
        logger.debug(f' consumption_metrics JSON #######: \n{consumption_metrics} ')
        data_json = json.loads(cons_json)
        for consumption in data_json:
            kwargs = {'timestamp':consumption[0],
                    'watt':consumption[1],
                    'device': device}
            logger.debug(f' Consumption JSON #######: \n{consumption} ')
                
                      
            fibaro.models.Consumption.objects.get_or_create(**kwargs) 
            logger.debug(f' Consumption Object #######: \n {kwargs} ')   
    logger.debug(f'______________________________________________ ')       