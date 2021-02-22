from fibaro.models import Room, Section
import json
from django.test import TestCase
from fibaro.models import Section

class SectionTest(TestCase):

    def setUp(self):
        file = open('./fibaro/samples/section.json')
        self.json_object = json.load(file)[0]
        

    def test_read_json(self):
        section = Section()
        section.read_json(self.json_object)

        self.assertEqual(3, len(self.json_object.keys()))
        self.assertEqual(9999, section.id)
        self.assertEqual('section_test', section.name)
        self.assertEqual(9999, section.sortOrder)