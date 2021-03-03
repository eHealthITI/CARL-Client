from django.test import TestCase

from fibaro.samples.devices import SampleDevices
from fibaro.validators import Device
from ypostirizoclient.settings import IGNORED_DEVICES as ignored


class FibaroDevicesTestCase(TestCase):

    def setUp(self):
        self.samples = SampleDevices()
        self.ignored_devices = ignored

    def test_door_sensor(self):
        device = Device(**self.samples.door_sensor)
        self.assertEqual(device.__class__, Device)

    def test_flood_sensor(self):
        device = Device(**self.samples.flood_sensor)
        self.assertEqual(device.__class__, Device)

    def test_light_sensor(self):
        device = Device(**self.samples.light_sensor)
        self.assertEqual(device.__class__, Device)

    def test_presence_sensor(self):
        device = Device(**self.samples.presence_sensor)
        self.assertEqual(device.__class__, Device)

    def test_red_button_sensor(self):
        device = Device(**self.samples.red_button_sensor)
        self.assertEqual(device.__class__, Device)

    def test_temp_sensor(self):
        device = Device(**self.samples.temp_sensor)
        self.assertEqual(device.__class__, Device)

    def test_devices_bulk(self):
        for dev in self.samples.valid_devices:
            if dev['type'] not in self.ignored_devices:
                device = Device(**dev)
                self.assertEqual(device.__class__, Device)
