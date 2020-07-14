import requests
from django.conf import settings
from .exceptions import InvalidToken, PageNotFound, CloudIsDown, EndpointNotImplemented

from fibaro.ypostirizo import Cloud


class HomecenterAdapter():
    """The class that describes functionality from homecenter
    to ypostirizoClient.
    """

    def __init__(self):
        """Basic data initialization"""
        Cloud.__init__(self)
        self.token = settings.HC_TOKEN
        self.url = settings.HC_URL
        self.user = settings.HC_USER

    def send(self, endpoint='/devices/', payload=None, method='GET'):
        """Send data [event] to ypostirizoCloud"""
        headers = {'authorization': f'{self.token}'}
        response = requests.request(method, self.url+endpoint,
                                    data=payload, headers=headers)

        if not response.ok:
            if response.status_code == 501:
                raise EndpointNotImplemented
            if response.status_code >= 500:
                raise CloudIsDown
            if response.status_code == 404:
                raise PageNotFound
            if response.json().get("detail") == 'Invalid token.':
                raise InvalidToken
            return response
        return response
