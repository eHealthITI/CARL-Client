from fibaro.fibaro import HomeCenter
import requests
from django.conf import settings
from .exceptions import InvalidToken, PageNotFound, CloudIsDown


class HCAdapter():
    """The class that describes functionality from homecenter
    to ypostirizoClient.
    """

    def __init__(self):
        """Basic data initialization"""
        self.token = settings.HC_TOKEN
        self.url = settings.HC_URL
