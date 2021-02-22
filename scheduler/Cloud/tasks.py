import json
import logging
from datetime import datetime

from celery import Celery
import fibaro.models
from fibaro.ypostirizo import Cloud
from ypostirizoclient import settings

app = Celery('tasks', broker='redis://localhost:6379//')


@app.task(rate_limit='5/h')
def update_devices():
    """
    Async tasks that pushes data (on a scheduled basis) regarding
    the devices from local DB to YpostiriZO Cloud.
    """
    cloud = Cloud()
    latest_devices = fibaro.models.Device.objects.all()
    device_list = []
    if latest_devices:
        for dev in latest_devices:
            props = json.loads(dev.properties)
            if dev.type not in settings.IGNORED_DEVICES:

                if props['batteryLevel'] == "255":
                    props['batteryLevel'] = 1

                device = {'type': settings.TYPE_OF_CHOICES[dev.baseType],
                          'serial': props.get('serialNumber'),
                          'make': props.get('zwaveCompany'),
                          'model': dev.type,
                          'battery': props.get('batteryLevel'),
                          'mac': None,
                          'id': dev.id}

                device_list.append(device)

        response = cloud.send(endpoint='/api/device/devices/register_device/',
                   payload=json.dumps(device_list))

        logging.info("Response from Cloud : {}".format(response))


@app.task
def upload_events():
    """
    Async tasks that pushes data (on a scheduled basis) regarding
    the events from local DB to YpostiriZO Cloud.
    """
    cloud = Cloud()
    current_time = int(datetime.now().timestamp())
    latest_events = fibaro.models.EventBase.objects.filter(timestamp__gte=current_time - 600).order_by('pk')
    event_list = []
    if latest_events:
        for ev in latest_events:
            event = {'device': ev.deviceID, 'timestamp': ev.timestamp,
                     'id': ev.pk, 'event_type': ev.event,
                     'value': ev.value}
            event_list.append(event)
        response = cloud.send(endpoint='/api/device/events/new_event/',
                   payload=json.dumps(event_list))
        logging.info("Response from Cloud : {}".format(response))