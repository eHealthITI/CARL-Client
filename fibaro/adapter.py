import requests
from django.conf import settings
from .exceptions import InvalidToken, PageNotFound


class Cloud():
    """The class that describes functionality from ypostirizoClient
    to ypostirizoCloud.
    """

    def __init__(self):
        """Basic data initialization"""
        self.token = settings.CLOUD_TOKEN
        self.url = settings.CLOUD_URL

    def send(self, endpoint='/device/events/', payload=None, method='GET'):
        """Send data [event] to ypostirizoCloud"""
        headers = {'authorization': f'Token {self.token}'}
        response = requests.request(method, self.url+endpoint,
                                    data=payload, headers=headers)
        # TODO exceptions, tests,
        if not response.ok:
            if response.status_code == 404:
                raise PageNotFound
            if response.json().get("detail") == 'Invalid token.':
                raise InvalidToken
            return response
        return response
