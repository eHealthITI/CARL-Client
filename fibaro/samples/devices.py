import json


class SampleDevices:

    def __init__(self):
        with open("fibaro/samples/devices/devices.json") as resp:
            self.valid_devices = json.load(resp)

        with open("fibaro/samples/devices/doorSensor.json") as resp:
            self.door_sensor = json.load(resp)[0]

        with open("fibaro/samples/devices/floodSensor.json") as resp:
            self.flood_sensor = json.load(resp)[0]

        with open("fibaro/samples/devices/lightSensor.json") as resp:
            self.light_sensor = json.load(resp)[0]

        with open("fibaro/samples/devices/presenceSensor.json") as resp:
            self.presence_sensor = json.load(resp)[0]

        with open("fibaro/samples/devices/redButtonSensor.json") as resp:
            self.red_button_sensor = json.load(resp)[0]

        with open("fibaro/samples/devices/tempSensor.json") as resp:
            self.temp_sensor = json.load(resp)[0]
