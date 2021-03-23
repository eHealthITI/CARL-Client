import json
import logging
from django.contrib.postgres.fields import JSONField, ArrayField
from django.db import models
from scheduler.Fibaro import tasks as fibaro


class Section(models.Model):
    """
        This model is used to represent the section data that are fetched from the HCL API.

    Args:
        id: Integer This is the same as the section's id on the HCL 
        name: Text e.g. First Floor
        sortOrder: Integer
    """
    id = models.IntegerField(primary_key=True)
    name = models.TextField()
    sortOrder = models.IntegerField(null=True)



    """
        Acts as a serializer and maps the data fetched from HCL's API to the variables 
        of a Section instance.
        
        Args:
            section_dict: dictionary of a single Section element returned from HCL's API
    """
    def read_json(self, section_dict):
            self.id = section_dict.get('id')
            self.name = section_dict.get('name')
            self.sortOrder = section_dict.get('sortOrder')

class Room(models.Model):
    """
        This model is used to represent the room data that are fetched from the HCL API.

    Args:
        id: Integer This is the same as the room's id on the HCL
        name: Test e.g Living Room
        SectionID: Foreign key for Section where the room belongs to
        defaultSensors: List of dictionaries with sensor data
        defaultThermostat: Integer representing which element in defaultSensors concerns the defaultThermostat
        created: Integer representing the creation datetime in unix epoch e.g. 12314654    
        modified: Integer representing the datetime of last modification in unix epoch e.g. 12314654    
        sortOrder: Integer

    """
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

    def read_json(self, room_dict):
        """
        Acts as a serializer and maps the data fetched from HCL's API to the variables 
        of a Section instance.
        

        Args:
            rooms (undefined):
                section_dict: dictionary of a single Section element returned from HCL's API
        """
        try:
            self.id = room_dict.get('id')
            self.name = room_dict.get('name')
            self.sectionID = Section.objects.get(pk=room_dict.get('sectionID'))
            self.icon = room_dict.get('icon')
            self.defaultSensors = room_dict.get('defaultSensors')
            self.defaultThermostat = room_dict.get('defaultThermostat')
            self.created = room_dict.get('created')
            self.modified = room_dict.get('modified')
            self.sortOrder = room_dict.get('sortOrder')
        except Section.DoesNotExist:
            logging.info("SectionID:{} --- Does NOT exist ".format(room_dict.get('sectionID')))
            fibaro.get_sections()


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

    def read_json(self, device_dict):
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
            fibaro.get_rooms()
        except Device.DoesNotExist:
            logging.info("DeviceID:{} --- Does NOT exist ".format(device_dict.get('parentID')))
            fibaro.get_sensor_data()


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
    synced = models.BooleanField(default=False)

    def read_json(self, event_dict):

        try:
            self.id = event_dict.get('id')
            self.type = event_dict.get('type')
            self.timestamp = event_dict.get('timestamp')
            self.deviceID = Device.objects.get(pk=event_dict.get('deviceID'))
            self.deviceType = event_dict.get('deviceType')
            self.property_name = event_dict.get('propertyName')
            self.newValue = event_dict.get('newValue')
            self.oldValue = event_dict.get('oldValue')
            self.synced = False
        except models.ObjectDoesNotExist:
            logging.info("Device ID:{}".format(event_dict.get('deviceID')))
            fibaro.get_sensor_data()
