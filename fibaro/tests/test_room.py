from fibaro.models import Room, Section
import json
from django.test import TestCase


class RoomTest(TestCase):

    def setUp(self):
        room_file = open('./fibaro/samples/room.json')
        self.json_room = json.load(room_file)[0]

        section_file = open('./fibaro/samples/section.json')
        json_section = json.load(section_file)[0]
        Section.objects.create(**json_section)

    def test_read_json(self):
        room = Room()
        room.read_json(self.json_room)

        self.assertEqual(9999, room.id)
        self.assertEqual('test_room', room.name)
        self.assertEqual(Section.objects.get(pk=9999), room.sectionID)
        self.assertEqual("room_baczek", room.icon)
        self.assertDictEqual({"temperature": 99,
                              "humidity": 99 , 
                              "light": 99
                              },room.defaultSensors)
        self.assertEqual(0, room.defaultThermostat)
        self.assertEqual(1, room.sortOrder)