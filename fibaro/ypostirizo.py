import logging
from re import L
import requests
from django.conf import settings
from fibaro.exceptions import InvalidToken, PageNotFound, CloudIsDown, EndpointNotImplemented
import json

class Cloud:
    """The class that describes functionality from ypostirizoClient
    to ypostirizoCloud.
    """

    def __init__(self):
        """Basic data initialization"""
        self.token = settings.CLOUD_TOKEN
        self.url = settings.CLOUD_URL
        self.headers = {'Authorization': f'Token {self.token}'}
    
    def send(self, endpoint='',
             payload='{}'):
        """
        Sends list of EventBase objects to the cloud in json
        format.
        """
        final_url = self.url + endpoint

 
        
        response = requests.post(url=final_url,
                                 json=json.dumps(payload),
                                 headers=self.headers,
                                 allow_redirects=False)
    
        
        
        
        
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
        else:
            return response.status_code