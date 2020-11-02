import json
import logging

from django.contrib.postgres.fields import JSONField
from django.db import models

from scheduler.tasks import find_devices


class Device(models.Model):
    id = models.IntegerField(primary_key=True)
    name = models.TextField()
    room_id = models.IntegerField()
    device_type = models.TextField()
    baseType = models.TextField()
    enabled = models.BooleanField()
    visible = models.BooleanField()
    is_plugin = models.BooleanField()
    parent_id = models.IntegerField()
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
        self.room_id = device_dict.get('roomID')
        self.device_type = device_dict.get('type')
        self.baseType = device_dict.get('baseType')
        self.enabled = device_dict.get('enabled')
        self.visible = device_dict.get('visible')
        self.is_plugin = device_dict.get('isPlugin')
        self.parent_id = device_dict.get('parentId')
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
    property_name = models.TextField()
    value = models.IntegerField()
    event = models.TextField(null=True)

    def read_json(self, event_dict):
        try:
            self.event_id = event_dict.get('id')
            self.event_type = event_dict.get('type')
            self.timestamp = event_dict.get('timestamp')
            self.device_id = Device.objects.get(pk=event_dict.get('deviceID'))
            self.device_type = event_dict.get('deviceType')
            self.property_name = event_dict.get('propertyName')
            self.value = event_dict.get('newValue')
            self.event = event_dict.get('event').get('data').get('keyAttribute')
        except models.ObjectDoesNotExist:
            logging.info("Device ID:{}".format(event_dict.get('deviceID')))
            find_devices()
