from random import choices
import string

import requests

from .models import *
from decimal import *

from channels.layers import get_channel_layer
from asgiref.sync import async_to_sync
from django.utils import timezone
from datetime import timedelta
from django.template.loader import render_to_string

import logging
from uuid import uuid4
from django.core.files import File
import os


logger = logging.getLogger(__name__)


channel_layer = get_channel_layer()



def send_to_all_users_websocket_notify(event, event_id, text=''):
    async_to_sync(channel_layer.group_send)('users',
                                            {"type": "user.notify",
                                             'event': event,
                                             'event_id': event_id,
                                             'message': text})


def send_to_user_websocket_notify(user, event, event_id, text):
    if user.channel:
        async_to_sync(channel_layer.send)(user.channel,
                                          {
                                              "type": "user.notify",
                                              'message': text,
                                              'event': event,
                                              'event_id': event_id
                                          })

