import json
import logging
from datetime import datetime

from celery import Celery
import fibaro.models
from fibaro.ypostirizo import Cloud
from ypostirizoclient import settings

app = Celery('tasks', broker='redis://localhost:6379//')


@app.task
def update_devices():
    cloud = Cloud()
    current_time = int(datetime.now().timestamp())
    #latest_devices = fibaro.models.Device.objects.filter(created__gt=current_time - settings.DB_EVENT_INTERVAL)
    latest_devices = fibaro.models.Device.objects.all()
    device_list = []
    if latest_devices:
        for dev in latest_devices:
            props = json.loads(dev.properties)
            if dev.device_type not in settings.IGNORED_DEVICES:
                device = {'type_of': settings.TYPE_OF_CHOICES[dev.baseType],
                          'serial': props.get('serialNumber'),
                          'make': props.get('zwaveCompany'),
                          'model': dev.device_type,
                          'battery': props.get('batteryLevel'),
                          'mac': None,
                          'id': dev.id}

                device_list.append(device)

        cloud.send(endpoint='/api/device/devices/register_device/',
                   payload=json.dumps(device_list))


@app.task
def upload_events():
    cloud = Cloud()
    current_time = int(datetime.now().timestamp())
    latest_events = fibaro.models.EventBase.objects.filter(timestamp__gte=current_time - settings.DB_EVENT_INTERVAL)
    event_list = []
    if latest_events:
        for ev in latest_events:
            event = {'device': ev.device_id, 'timestamp': ev.timestamp,
                     'id': ev.pk, 'event_type': ev.event,
                     'value': ev.value}
            event_list.append(event)
        cloud.send(endpoint='/api/device/events/new_event/',
                   payload=json.dumps(event_list))
