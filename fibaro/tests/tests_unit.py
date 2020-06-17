from django.test import TestCase
from fibaro.validators import Event
from fibaro.samples.events import SampleEvents
import pydantic


class FibaroTestCase(TestCase):
    """Simple test case for basic functionality"""

    def setUp(self):
        self.samples = SampleEvents()

    def test_valid_event(self):
        event = Event(**self.samples.valid_event)
        self.assertEqual(event.__class__, Event)

    def test_invalid_event(self):
        self.assertRaises(pydantic.ValidationError, Event, **self.samples.invalid_event)
