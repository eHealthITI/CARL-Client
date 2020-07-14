from django.conf import settings
from fibaro.ypostirizo import Cloud

import base64


class HomecenterAdapter(Cloud):
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

        self.token = f'Basic {encoded}'

    def get(self, endpoint='/panels/event', payload=None, method='GET', params=None):
        headers = {
            'accept': "application/json",
            'x-fibaro-version': "2",
            'accept-language': "en",
            'authorization': f"Basic  {self.token}"
        }
        return super(HomecenterAdapter, self).send(
            endpoint=endpoint, payload=payload,
            method=method, headers=headers, qs=params
        )
