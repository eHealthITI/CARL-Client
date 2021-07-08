import json
import logging
from datetime import datetime

from celery import Celery
import fibaro.models
from fibaro.ypostirizo import Cloud
from ypostirizoclient import settings
import pytz
import requests

app = Celery('tasks', broker='redis://localhost:6379//')


@app.task()
def update_devices():
    """
    Async tasks that pushes data (on a scheduled basis) regarding
    the devices from local DB to YpostiriZO Cloud.
    """

    cloud = Cloud()
    latest_devices = fibaro.models.Device.objects.all().exclude(
        type__in=settings.IGNORED_DEVICES).order_by('pk')

    device_list = []
    props = None
    if latest_devices:
        for dev in latest_devices:
            try:

                if type(dev.properties) is dict:
                    props = json.loads(json.dumps(props))
                else:
                    props = json.loads(dev.properties)

                device = {
                    "pk": dev.id,
                    "model": dev.type,
                    "name": dev.name,
                    "room": dev.roomID_id,
                    "parentId": dev.parentId_id,
                    "type_of":  settings.TYPE_OF_CHOICES[dev.baseType],
                    "enabled": dev.enabled,
                    #"wake_up_time": props['wakeUpTime'],
                    "categories": props['categories'],
                    "configured": props['configured'],
                    "dead": props['dead'],
                    "dead_reason": props['deadReason'],
                    "created": dev.created,
                    "modified": dev.modified,
                    # The serial number is the string fibaro00 concatenated with the id of the device.
                    "serial": "fibaro00{}".format(str(dev.id)),
                    "make": "Fibaro",
                    "last_sync_time": str(datetime.now(pytz.utc)),
                    #"battery": props['batteryLevel']
                }

                if fibaro.models.Device.objects.get(pk=dev.parentId_id).type in settings.IGNORED_DEVICES or device['parentId']==1:
                    del device['parentId']
                try :
                    if 'wakeUpTime' in props.keys() and 'batteryLevel' in props.keys():
                        device['wake_up_time'] = props['wakeUpTime']
                        device['battery'] = props['batteryLevel']
                    else:
                        print(device)
                        device['wake_up_time'] = 0
                        device['battery'] = 0
                except KeyError as e:
                    print(e)
                    print('\n')
                    print(dev)
                    
                device_list.append(device)

            except TypeError as e:

                logging.info(
                    '---------- ERROR ------------- \n{}'.format(dev.properties))
                logging.info('{}'.format(type(dev.properties)))
                logging.info('{}'.format(e))
        response = cloud.send(endpoint='/api/device/register_device/',
                              payload=device_list)
        

        logging.info(
            "UPLOAD DEVICE: Response from Cloud : {}".format(response))


@app.task
def upload_events():
    """
    Async tasks that pushes data (on a scheduled basis) regarding
    the events from local DB to YpostiriZO Cloud.
    """
    cloud = Cloud()
    current_time = int(datetime.now().timestamp())
    latest_events = fibaro.models.EventBase.objects.filter(
        synced=False).order_by('pk')
    
    if latest_events:
        # Split the event list to chunks of 1000 length
        latest_events = [latest_events[x:x+1000] for x in range(0, len(latest_events), 1000)]
        for chunk in latest_events:
            event_list = []
            for ev in chunk:
                if fibaro.models.Device.objects.get(pk=ev.deviceID_id).type not in settings.IGNORED_DEVICES:
                    event = {'device': ev.deviceID_id, 'timestamp': ev.timestamp,
                            'id': ev.pk, 'type': ev.type,
                            'old_value': ev.oldValue,
                            'new_value':ev.newValue}
                    event_list.append(event)
                

            response = cloud.send(endpoint='/api/device/events/new_event/',
                              payload=event_list)
        if response==200:
            for ev in event_list:
                try:
                    e = fibaro.models.EventBase.objects.get(pk=ev['id'])
                    e.synced=True
                    e.save()
                except Exception as e:
                    print(e)
                else:            
                    logging.info(
                        "UPLOAD EVENTS: Response from Cloud : {}".format(response))


@app.task
def upload_sections():
    """
    Async tasks that pushes data (on a scheduled basis) regarding
    the fibaro's sections from local DB to YpostiriZO Cloud.
    """
    cloud = Cloud()
    current_time = int(datetime.now().timestamp())
    sections = fibaro.models.Section.objects.all().order_by('pk')
    section_list = []
    if sections:
        for sec in sections:
            section = {'id': sec.pk,
                       'name': sec.name}
            section_list.append(section)
        response = cloud.send(endpoint='/api/device/register_new_section/',
                              payload=section_list)
        logging.info(
            "UPLOAD SECTIONS: Response from Cloud : {}".format(response))


@app.task
def upload_rooms():
    """
    Async tasks that pushes data (on a scheduled basis) regarding
    the fibaro's rooms from local DB to YpostiriZO Cloud.
    """
    cloud = Cloud()
    current_time = int(datetime.now().timestamp())
    rooms = fibaro.models.Room.objects.all().order_by('pk')
    room_list = []
    if rooms:
        for room in rooms:
            r = {'id': room.pk,
                 'name': room.name,
                 'section': room.sectionID_id}
            room_list.append(r)
        response = cloud.send(endpoint='/api/device/register_new_room/',
                              payload=room_list)
        logging.info("UPLOAD ROOM: Response from Cloud : {}".format(response))


def upload_consumption():
    cloud = Cloud()
    latest_consumptions = fibaro.models.Consumption.objects.filter(synced=False).order_by('pk')
    data = []
    if latest_consumptions:
        latest_consumptions = [latest_consumptions[x:x+1000] for x in range(0, len(latest_consumptions), 1000)]       
        for chunk in latest_consumptions:
            consumption_list = []
            for consumption in chunk:
                cons = {'device': consumption.device.id, 'timestamp': consumption.timestamp,
                            'watt': consumption.watt}
                data.append(cons)

            response = cloud.send(endpoint='/api/device/fibaro-consumption/',
                                  payload=data)
            print(response)

@app.task
def download_update():
    token = settings.CLOUD_TOKEN
    url = settings.CLOUD_URL
    headers = {'Authorization': f'Token {token}'}
    
    r = requests.get(url, headers=headers)
    
    with open('/latest.zip', 'wb') as f:
        for chunk in r.iter_content(chunk_size=1024): 
            if chunk: # filter out keep-alive new chunks
                f.write(chunk)
                


