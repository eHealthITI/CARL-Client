import json
import logging
from django.contrib.postgres.fields import JSONField, ArrayField
from django.db import models
from scheduler.Fibaro import tasks as fibaro


class Section(models.Model):
    id = models.IntegerField(primary_key=True)
    name = models.TextField()
    sort_order = models.IntegerField(null=True)

    def read_json(self, event_dict):
        self.id = event_dict.get('id')
        self.name = event_dict.get('name')
        self.sort_order = event_dict.get('SortOrder')


class Room(models.Model):
    id = models.IntegerField(primary_key=True)
    name = models.TextField()
    scene = models.ForeignKey(Section, on_delete=models.CASCADE)
    icon = models.TextField(null=True)
    default_sensors = ArrayField(models.IntegerField(null=True, blank=True), null=True)
    default_thermostat = models.IntegerField(null=True)  # It's the position of the object in the array defaultSensors.
    created = models.IntegerField(null=True)
    modified = models.IntegerField(null=True)
    sort_order = models.IntegerField(null=True)

    def read_json(self, rooms):
        try:
            self.id = rooms.get('id')
            self.name = rooms.get('name')
            self.section = Section.objects.get(pk=rooms.get('sectionID'))
            self.icon = rooms.get('icon')
            self.default_sensors = rooms.get('defaultSensors')
            self.default_thermostat = self.default_sensors[rooms.get('defaultThermostat')]
            self.created = rooms.get('created')
            self.modified = rooms.get('modified')
            self.sort_order = rooms.get('sortOrder')
        except models.ObjectDoesNotExist:
            logging.info("Device ID:{}".format(rooms.get('deviceID')))
            fibaro.get_sensor_data()


class Device(models.Model):
    id = models.IntegerField(primary_key=True)
    name = models.TextField()
    room = models.ForeignKey(Room, on_delete=models.CASCADE)
    device_type = models.TextField()
    baseType = models.TextField()
    enabled = models.BooleanField()
    visible = models.BooleanField()
    is_plugin = models.BooleanField()
    parent_id = models.ForeignKey('self', on_delete=models.CASCADE, related_name='device', null=True)
    remote_gateway_id = models.IntegerField(null=True)
    view_xml = models.BooleanField(null=True)
    config_xml = models.BooleanField(null=True)
    interfaces = JSONField()
    properties = JSONField()
    actions = JSONField()
    created = models.IntegerField()
    modified = models.IntegerField()
    sort_order = models.IntegerField()

    def read_json(self, device_dict):
        self.id = device_dict.get('id')
        self.name = device_dict.get('name')
        self.room = device_dict.get('roomID')
        self.device_type = device_dict.get('type')
        self.baseType = device_dict.get('baseType')
        self.enabled = device_dict.get('enabled')
        self.visible = device_dict.get('visible')
        self.is_plugin = device_dict.get('isPlugin')
        self.parent_id = Device.objects.get(pk=device_dict.get('parentId'))
        self.remote_gateway_id = device_dict.get('remoteGatewayId')
        self.view_xml = device_dict.get('viewXml')
        self.config_xml = device_dict.get('configXml')
        self.interfaces = json.dumps(device_dict.get('interfaces'))
        self.actions = json.dumps(device_dict.get('actions'))
        self.created = device_dict.get('created')
        self.modified = device_dict.get('modified')
        self.sort_order = device_dict.get('sortOrder')
        self.properties = json.dumps(device_dict.get('properties'))


class EventBase(models.Model):
    event_id = models.IntegerField(primary_key=True)
    event_type = models.TextField()
    timestamp = models.IntegerField()
    device = models.ForeignKey(Device, on_delete=models.CASCADE)
    device_type = models.TextField()
    property_name = models.TextField(null=True)
    value = models.FloatField(null=True)
    event = models.TextField(null=True)

    def read_json(self, event_dict):
        try:
            self.event_id = event_dict.get('id')
            self.event_type = event_dict.get('type')
            self.timestamp = event_dict.get('timestamp')
            self.device = Device.objects.get(pk=event_dict.get('deviceID'))
            self.device_type = event_dict.get('deviceType')
            self.property_name = event_dict.get('propertyName')
            self.value = event_dict.get('newValue')
            if 'event' in event_dict.keys():
                self.event = event_dict.get('event').get('data').get('keyAttribute')
            else:
                self.event = None
        except models.ObjectDoesNotExist:
            logging.info("Device ID:{}".format(event_dict.get('deviceID')))
            fibaro.get_sensor_data()
