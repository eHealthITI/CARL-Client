import json


class SampleEvents:

    def __init__(self):
        with open("fibaro/samples/responses.json") as resp:
            self.valid_events = json.load(resp)

        with open("fibaro/samples/invalidResponses.json") as invs:
            self.invalid_events = json.load(invs)

        with open('fibaro/samples/lightSensor.json') as light:
            self.light_event = json.load(light)[0]

        with open('fibaro/samples/presenceSensor.json') as pres:
            self.presence_event = json.load(pres)[0]

        with open('fibaro/samples/tempSensor.json') as temp:
            self.temp_event = json.load(temp)[0]
