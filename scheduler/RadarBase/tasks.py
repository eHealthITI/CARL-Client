import base64
import json
import logging
from datetime import datetime

from celery import Celery
from django.core import serializers
from django.db.models import Max

from fibaro.adapter import HomeCenterAdapter
import fibaro.models
from fibaro.ypostirizo import Cloud
from ypostirizoclient import settings

app = Celery('tasks', broker='redis://localhost:6379//')

class RadarBaseTasks:
    @app.task
    def send_to_radar_base(self):
        # this task is going to be used to send the data to the cloud
        pass
