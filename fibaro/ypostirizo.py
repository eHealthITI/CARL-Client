import logging

from fibaro.validators import EventBase
import requests

from django.conf import settings
from fibaro.exceptions import InvalidToken, PageNotFound, CloudIsDown, EndpointNotImplemented


class Cloud:
    """The class that describes functionality from ypostirizoClient
    to ypostirizoCloud.
    """

    def __init__(self):
        """Basic data initialization"""
        self.token = settings.CLOUD_TOKEN
        self.url = settings.CLOUD_URL
        self.headers = {'authorization': f'Token {self.token}'}

    def send(self, endpoint=None,
             payload=None):
        """
        Sends list of EventBase objects to the cloud in json
        format.
        """

        response = requests.request(method='POST',
                                    url=self.url+endpoint,
                                    data=payload,
                                    headers=self.headers)

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


