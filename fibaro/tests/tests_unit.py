from django.conf import settings
from django.test import TestCase

import pydantic
import pytest

from fibaro.samples.events import SampleEvents
from fibaro.validators import EventBase
from fibaro.ypostirizo import Ypostirizo


class FibaroTestCase(TestCase):
    """Simple test case for basic functionality"""

    def setUp(self):
        self.samples = SampleEvents()

    def test_temp_event(self):
        event = EventBase(**self.samples.temp_event)
        self.assertEqual(event.__class__, EventBase)

    def test_light_event(self):
        event = EventBase(**self.samples.light_event)
        self.assertEqual(event.__class__, EventBase)

    def test_presence_event(self):
        event = EventBase(**self.samples.presence_event)
        self.assertEqual(event.__class__, EventBase)

    def test_valid_events(self):
        for ev in self.samples.valid_events:
            event = EventBase(**ev)
            self.assertEqual(event.__class__, EventBase)

    def test_invalid_events(self):
        for ev in self.samples.invalid_events:
            self.assertRaises(pydantic.ValidationError, EventBase, **ev)


class YpostiriZOAdapterTestCase(TestCase):
    """Test the fibaro adapter (ypostirizo client -> ypostirizo cloud"""

    def setUp(self):
        self.samples = SampleEvents()

    @pytest.mark.skip('Skipping as an integration test')
    def test_valid_data(self):
        """test a valid event data object sent to the cloud"""
        response = Ypostirizo(self.samples.valid_events[0])._post()
        self.assertEqual(response.status_code, 201)

    @pytest.mark.skip('Skipping as an integration test')
    def test_invalid_token(self):
        """test a valid event data object sent to the cloud with wrong token"""
        oldToken = settings.CLOUD_TOKEN
        settings.CLOUD_TOKEN = 'A wrong token'
        response = Ypostirizo(self.samples.valid_events[0])._post()
        self.assertEqual(response.status_code, 401)
        settings.CLOUD_TOKEN = oldToken
