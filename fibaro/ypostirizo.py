import requests
from django.conf import settings

from fibaro.exceptions import CloudIsDown, InvalidToken, PageNotFound
from fibaro.validators import EventBase


class Cloud():
    """The class that describes functionality from ypostirizoClient
    to ypostirizoCloud.
    """

    def __init__(self):
        """Basic data initialization"""
        self.token = settings.CLOUD_TOKEN
        self.url = settings.CLOUD_URL

    def send(self, endpoint='/device/events/', payload=None,
             method='GET', headers=None, qs=None):
        """Send data [event] to ypostirizoCloud"""
        if not headers:
            headers = {'authorization': f'Token {self.token}'}
        response = requests.request(method, self.url+endpoint,
                                    data=payload, headers=headers, params=qs)
        if not response.ok:
            if response.status_code == 501:
                raise CloudIsDown
            if response.status_code == 404:
                raise PageNotFound
            if response.json().get("detail") == 'Invalid token.':
                raise InvalidToken
            return response
        return response


class Ypostirizo():
    """YpostiriZO adapter to push data to the cloud.
    initial_data: dict | EventBase Instance
    """

    def __init__(self, initial_data=None):
        self.event = EventBase(**initial_data)

    def _post(self):
        """Posts the self.event to the cloud to create a new event."""
        return Cloud().send(
            payload=self.event.dict(),
            method='POST'
        )
