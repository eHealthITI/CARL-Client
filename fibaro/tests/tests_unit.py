from django.test import TestCase
from fibaro.validators import Event
import pydantic


class FibaroTestCase(TestCase):
    """Simple test case for basic functionality"""

    def setUp(self):
        self.sample_valid_event = {
            "id": "8126",
            "type": "DEVICE_EVENT",
            "timestamp": 1404723546,
            "deviceID": 1701,
            "deviceType": "com.fibaro.temperatureSensor",
            "propertyName": "value",
            "oldValue": 28.6,
            "newValue": 26.7
        }
        self.sample_invalid_event = {
            "id": "8126",
            "type": None,
            "timestamp": "tasdf9845",
            "deviceID": 1701,
            "deviceType": "com.fibaro.temperatureSensor",
            "propertyName": "value",
            "oldValue": 28.6,
            "newValue": 26.7
        }

    def test_valid_event(self):
        event = Event(**self.sample_valid_event)
        self.assertEqual(event.__class__, Event)

    def test_invalid_event(self):
        self.assertRaises(pydantic.ValidationError, Event, **self.sample_invalid_event)
