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
        of a Room instance.


        Args:
            room_dict(dictionary):
                dictionary of a single room element returned from HCL's API

        Throw:
            It may throw models.Model.DoesNotExist if the Section is not present in the database. 
            Runs fibaro.get_sections() to get all the latest data from HCL regarding the sections.
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
            logging.info(
                "SectionID:{} --- Does NOT exist ".format(room_dict.get('sectionID')))
            fibaro.get_sections()


class Device(models.Model):
    """
    This model is used to represent the device data that are fetched from the HCL API.

    Inheritance:
        models.Model:

    Args: 
        id: Integer This is the same as the device's id on the HCL
        name: Text in the format of X.X.X. 
        roomID: Foreign key for Room where the device is registered to
        type: Text represting the model's funcionality 
            eg:
                com.fibaro.FGMS001v2
                com.fibaro.lightSensor 
                com.fibaro.seismometer 
        baseType: Text representing the type of the sensor eg: com.fibaro.multilevelSensor
        enabled: Boolean True if it is enabled
        visible: Boolean True if it is visible
        isPlugin: Boolen True if it is a plugin (this is never supposed to be true)
        parentId: Foreign key for its parents' id 
            keep in mind that if parentId is 0 it refers to the HCL Hub. The problem is that HCL hub uses the value 0 as null as well. 
        remoteGatewayId: Integer, most of the times has 0 as a value
        viewXml: Boolean
        configXml: Boolean
        interfaces: JSON 
        properties: JSON
        actions: JSON
        created: Integer representing the creation datetime in unix epoch e.g. 12314654    
        modified: Integer representing the datetime of last modification in unix epoch e.g. 12314654    
        sortOrder: Integer
        
    """
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
        """
        Acts as a serializer and maps the data fetched from HCL's API to the variables 
        of a Device instance.


        Args:
            device_dict (dictionary):
                device_dict: dictionary of a single room element returned from HCL's API

        Throw:
            It may throw models.Model.DoesNotExist if the ParentId, or the RoomId is not present in the database. 
            Runs fibaro.get_rooms() and fibaro.get_sensor_data(),  to get all the latest data from HCL regarding the sections.
        """
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
            logging.info(
                "RoomID:{} --- Does NOT exist ".format(device_dict.get('roomID')))
            fibaro.get_rooms()
        except Device.DoesNotExist:
            logging.info(
                "DeviceID:{} --- Does NOT exist ".format(device_dict.get('parentID')))
            fibaro.get_sensor_data()


class EventBase(models.Model):
    """
    This model is used to represent the Event data that are fetched from the HCL API.

    Inheritance:
        models.Model:
    Args:
        id (Integer): This is the same as the device's id on the HCL
        type (Text): The type of the stored event eg. DEVICE_PROPERTY_CHANGED
        timestamp (Integer): Represent the time when the event was registered, in unix epoch format eg. 13248655
        deviceId (Foreign Key): Which device registered the event on HCL.
        deviceType (Text): device's type field eg com.fibaro.lightSensor (this in not fetched from local database)
        propertyName (Text)
        oldValue (Float): represents the latest value before current event occured eg 22.0
        newValue (Float): represent the new value that was registered eg 24.0
        icon (Text):
        event (JSON): 
        synced (Boolean): if the event was pushed to the cloud it becomes True;
        
    """
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
        """
        Acts as a serializer and maps the data fetched from HCL's API to the variables 
        of a Event instance.


        Args:
            event_dict (dictionary):
                event_dict: dictionary of a single room element returned from HCL's API

        Throw:
            It may throw models.Model.DoesNotExist if the deviceID is not present in the database. 
            Runs fibaro.get_rooms() to get all the latest data from HCL regarding the sections.
        """

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


class Consumption(models.Model):
    timestamp = models.BigIntegerField()
    watt = models.FloatField()
    device = models.ForeignKey(Device,on_delete=models.DO_NOTHING)
    synced = models.BooleanField(default=False)