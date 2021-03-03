from fibaro.models import Device, EventBase
import json
from django.test import TestCase


class EventBaseTest(TestCase):

    def setUp(self):
        event_file = open('./fibaro/samples/tempSensor.json')
        self.json_event = json.load(event_file)[0]
        
    def test_read_json(self):
        event = EventBase()
        event.read_json(self.json_event)

        self.assertEqual(7826, event.id)
        self.assertEqual('DEVICE_PROPERTY_CHANGED', event.type)
        self.assertEqual(1594973502, event.timestamp)
        self.assertRaises(Device.DoesNotExist, Device.objects.get(pk=27))
        self.assertEqual("com.fibaro.temperatureSensor", event.deviceType)
        self.assertEqual("value", event.propertyName)
        self.assertEqual(26.5, event.oldValue)
        self.assertEqual(26.7, event.newValue)
        self.assertIsNone(event.icon)

