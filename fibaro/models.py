import json
import logging
from django.contrib.postgres.fields import JSONField, ArrayField
from django.db import models
from scheduler.Fibaro import tasks as fibaro


class Section(models.Model):
    id = models.IntegerField(primary_key=True)
    name = models.TextField()
    sortOrder = models.IntegerField(null=True)

    def read_json(self, section_dict):
            self.id = section_dict.get('id')
            self.name = section_dict.get('name')
            self.sortOrder = section_dict.get('sortOrder')

class Room(models.Model):
    id = models.IntegerField(primary_key=True)
    name = models.TextField()
    sectionID = models.ForeignKey(Section, on_delete=models.CASCADE)
    icon = models.TextField(null=True)
    defaultSensors = JSONField(null=True)
    # It's the position of the object in the array defaultSensors.
    defaultThermostat = models.IntegerField(null=True)
    created = models.IntegerField(null=True)
    modified = models.IntegerField(null=True)
    sortOrder = models.IntegerField(null=True)

    def read_json(self, rooms):
        try:
            self.id = rooms.get('id')
            self.name = rooms.get('name')
            self.sectionID = Section.objects.get(pk=rooms.get('sectionID'))
            self.icon = rooms.get('icon')
            self.defaultSensors = rooms.get('defaultSensors')
            self.defaultThermostat = rooms.get('defaultThermostat')
            self.created = rooms.get('created')
            self.modified = rooms.get('modified')
            self.sortOrder = rooms.get('sortOrder')
        except Section.DoesNotExist:
            logging.info("SectionID:{} --- Does NOT exist ".format(rooms.get('sectionID')))
            fibaro.get_sections.delay()


class Device(models.Model):
    id = models.IntegerField(primary_key=True)
    name = models.TextField()
    roomID = models.ForeignKey(Room, on_delete=models.CASCADE, null=True)
    type = models.TextField()
    baseType = models.TextField()
    enabled = models.BooleanField()
    visible = models.BooleanField()
    isPlugin = models.BooleanField()
    parentId = models.ForeignKey('self',
                                 on_delete=models.CASCADE,
                                 related_name='device',
                                 null=True)
    remoteGatewayId = models.IntegerField(null=True)
    viewXml = models.BooleanField(null=True)
    configXml = models.BooleanField(null=True)
    interfaces = JSONField()
    properties = JSONField()
    actions = JSONField()
    created = models.IntegerField()
    modified = models.IntegerField()
    sortOrder = models.IntegerField()

    def __init__(self, device_dict):
        try:
            self.id = device_dict.get('id')
            self.name = device_dict.get('name')
            self.roomID = Room.objects.get(pk=device_dict.get('roomID'))
            self.type = device_dict.get('type')
            self.baseType = device_dict.get('baseType')
            self.enabled = device_dict.get('enabled')
            self.visible = device_dict.get('visible')
            self.isPlugin = device_dict.get('isPlugin')
            self.parentId = Device.objects.get(pk=device_dict.get('parentId'))
            self.remoteGatewayId = device_dict.get('remoteGatewayId')
            self.viewXml = device_dict.get('viewXml')
            self.configXml = device_dict.get('configXml')
            self.interfaces = json.dumps(device_dict.get('interfaces'))
            self.actions = json.dumps(device_dict.get('actions'))
            self.created = device_dict.get('created')
            self.modified = device_dict.get('modified')
            self.sortOrder = device_dict.get('sortOrder')
            self.properties = json.dumps(device_dict.get('properties'))
        except Room.DoesNotExist:
            logging.info("RoomID:{} --- Does NOT exist ".format(device_dict.get('roomID')))
            fibaro.get_rooms.delay()
        except Device.DoesNotExist:
            logging.info("DeviceID:{} --- Does NOT exist ".format(device_dict.get('parentID')))
            fibaro.get_sensor_data.delay()


class EventBase(models.Model):
    id = models.IntegerField(primary_key=True)
    type = models.TextField()
    timestamp = models.IntegerField()
    deviceID = models.ForeignKey(Device, on_delete=models.CASCADE)
    deviceType = models.TextField()
    propertyName = models.TextField(null=True)
    oldValue = models.FloatField(null=True)
    newValue = models.FloatField(null=True)
    icon = models.TextField(null=True)
    event = JSONField(null=True)

    def read_json(self, event_dict):

        try:
            self.id = event_dict.get('id')
            self.type = event_dict.get('type')
            self.timestamp = event_dict.get('timestamp')
            self.deviceID = Device.objects.get(pk=event_dict.get('deviceID'))
            self.deviceType = event_dict.get('deviceType')
            self.property_name = event_dict.get('propertyName')
            self.value = event_dict.get('newValue')
        except models.ObjectDoesNotExist:
            logging.info("Device ID:{}".format(event_dict.get('deviceID')))
            fibaro.get_sensor_data()
