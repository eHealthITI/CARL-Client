class SampleEvents:

    def __init__(self):
        self.valid_event = {
            "id": "8126",
            "type": "DEVICE_EVENT",
            "timestamp": 1404723546,
            "deviceID": 1701,
            "deviceType": "com.fibaro.temperatureSensor",
            "propertyName": "value",
            "oldValue": 28.6,
            "newValue": 26.7
        }

        self.invalid_event = {
            "id": "8126",
            "type": None,
            "timestamp": "tasdf9845",
            "deviceID": 1701,
            "deviceType": "com.fibaro.temperatureSensor",
            "propertyName": "value",
            "oldValue": 28.6,
            "newValue": 26.7
        }
