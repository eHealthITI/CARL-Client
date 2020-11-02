from django.conf import settings
from fibaro.ypostirizo import Cloud

import base64


class HomeCenterAdapter(Cloud):
    """The class that describes functionality from homecenter
    to ypostirizoClient.
    """

    def __init__(self):
        """Basic data initialization"""
        Cloud.__init__(self)
        self.password = settings.HC_PASSWORD
        self.url = settings.HC_URL
        self.user = settings.HC_USER

        hash_constructor = self.user+':'+self.password
        to_encode = hash_constructor.encode('ascii')
        encoded = base64.b64encode(to_encode).decode('utf-8')

        self.token = encoded

    def get(self, endpoint='/api/devices', payload=None, method='GET', params=None):
        headers = {
            'accept': "application/json",
            'x-fibaro-version': "2",
            'accept-language': "en",
            'authorization': f"Basic  {settings.HC_TOKEN}"
        }
        return super(HomeCenterAdapter, self).send(
            endpoint=endpoint, payload=payload,
            method=method, headers=headers, qs=params
        )

    def push(self, payload):
        """Receive data from Home center
        and push them to YpostiriZO Cloud."""
        headers = {
            'Authorization': f"Token {settings.CLOUD_TOKEN}"
        }
        response = Cloud.send(self, headers=headers, endpoint="/api/device/events/new_event/", payload=payload)
        return response

