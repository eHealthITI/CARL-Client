from django.conf import settings


class HCAdapter():
    """The class that describes functionality from homecenter
    to ypostirizoClient.
    """

    def __init__(self):
        """Basic data initialization"""
        self.token = settings.HC_TOKEN
        self.url = settings.HC_URL
