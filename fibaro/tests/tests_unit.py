from django.test import TestCase
from fibaro.ypostirizo import Ypostirizo
from fibaro.validators import EventBase
from fibaro.samples.events import SampleEvents
from django.conf import settings
import pydantic


class FibaroTestCase(TestCase):
    """Simple test case for basic functionality"""

    def setUp(self):
        self.samples = SampleEvents()

    def test_valid_event(self):
        for ev in self.samples.valid_events:
            event = EventBase(**ev)
            self.assertEqual(event.__class__, EventBase)

    def test_invalid_event(self):
        for ev in self.samples.invalid_events:
            self.assertRaises(pydantic.ValidationError, EventBase, **ev)


class FibaroAdapter(TestCase):
    """Test the fibaro adapter (ypostirizo client -> ypostirizo cloud"""

    def setUp(self):
        self.samples = SampleEvents()

    def test_valid_data(self):
        """test a valid event data object sent to the cloud"""
        response = Ypostirizo(self.samples.valid_event)._post()
        self.assertEqual(response.status_code, 201)

    def test_invalid_token(self):
        """test a valid event data object sent to the cloud with wrong token"""
        oldToken = settings.CLOUD_TOKEN
        settings.CLOUD_TOKEN = 'A wrong token'
        response = Ypostirizo(self.samples.valid_event)._post()
        self.assertEqual(response.status_code, 401)
        settings.CLOUD_TOKEN = oldToken
