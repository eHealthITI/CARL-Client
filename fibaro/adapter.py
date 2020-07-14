from django.conf import settings
from fibaro.ypostirizo import Cloud


class HomecenterAdapter(Cloud):
    """The class that describes functionality from homecenter
    to ypostirizoClient.
    """

    def __init__(self):
        """Basic data initialization"""
        Cloud.__init__(self)
        self.token = settings.HC_TOKEN
        self.url = settings.HC_URL
        self.user = settings.HC_USER

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
