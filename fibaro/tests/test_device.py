import json
from django.test import TestCase

from fibaro.samples.devices import SampleDevices
from fibaro.models import Device, Room, Section
from ypostirizoclient.settings import IGNORED_DEVICES as ignored


class DeviceTest(TestCase):

    def setUp(self):
        room_file = open('./fibaro/samples/room.json')
        json_room = json.load(room_file)[0]

    def test_door_sensor(self):
        device_file = open('./fibaro/samples/devices/doorSensor.json')
        json_door_sensor = json.load(device_file)[0]
        device = Device()
        device.read_json(json_door_sensor)

        self.assertEqual(27, device.id)
        self.assertEqual( device.roomID)
        self.assertEqual('Cupdoor', device.name)
        self.assertEqual('com.fibaro.FGDW002', device.type)
        self.assertEqual('com.fibaro.doorWindowSensor', device.baseType)
        self.assertTrue(device.enabled)
        self.assertTrue(device.visible)
        self.assertFalse(device.isPlugin)
        self.assertFalse(device.isPlugin)
        self.assertIsNone(device.parentId) # the parent id is 26 which does not exist. Although is nullable added DoesNotExist exc.
        self.assertIsNone(device.remoteGatewayId) # is nullable
        self.assertFalse(device.viewXml) 
        self.assertFalse(device.configXml) 
        self.assertListEqual(["battery", "fibaroBreach", "fibaroFirmwareUpdate",
                              "tamper", "zwave", "zwaveAlarm", 
                              "zwaveMultiChannelAssociation", "zwaveWakeup"], device.interfaces) 
        self.assertDictEqual({
          "abortUpdate": 1,
          "reconfigure": 0,
          "retryUpdate": 1,
          "setInterval": 1,
          "startUpdate": 1,
          "updateFirmware": 1
        }, device.actions)
        self.assertEqual(1594207736, device.created)
        self.assertEqual(12, device.sortOrder)
        self.assertDictEqual({
          "pollingTimeSec": 0,
          "wakeUpTime": 21600,
          "zwaveCompany": "Fibargroup",
          "zwaveInfo": "3,4,38",
          "zwaveVersion": "3.2",
          "alarmLevel": 0,
          "alarmType": 0,
          "batteryLevel": 90,
          "batteryLowNotification": true,
          "categories": [
            "security"
          ],
          "configured": true,
          "dead": false,
          "deadReason": "",
          "defInterval": 0,
          "deviceControlType": 0,
          "deviceIcon": 120,
          "emailNotificationID": 0,
          "emailNotificationType": 0,
          "endPointId": 0,
          "firmwareUpdate": {
            "info": "",
            "progress": 0,
            "status": "UpToDate",
            "updateVersion": "3.2"
          },
          "lastBreached": 1594208537,
          "log": "",
          "logTemp": "",
          "manufacturer": "",
          "markAsDead": true,
          "maxInterval": 0,
          "minInterval": 0,
          "model": "",
          "nodeId": 3,
          "parametersTemplate": 802,
          "pendingActions": false,
          "productInfo": "1,15,7,2,16,0,3,2",
          "pushNotificationID": 0,
          "pushNotificationType": 0,
          "saveLogs": true,
          "serialNumber": "h'0000000000026a72",
          "smsNotificationID": 0,
          "smsNotificationType": 0,
          "stepInterval": 0,
          "tamper": true,
          "updateVersion": "",
          "useTemplate": true,
          "userDescription": "",
          "value": false
        }, device.properties)


