
from django.utils import timezone
from datetime import timedelta

from django.contrib.auth import authenticate, get_user_model
from django.contrib.auth.password_validation import validate_password
from django.core import exceptions as django_exceptions
from django.db import IntegrityError, transaction

from rest_framework import exceptions, serializers, status, generics
from .models import *
from user.serializers import UserSaveSerializer

from django.contrib.auth.tokens import default_token_generator


import logging
logger = logging.getLogger(__name__)


class ClientContactSerializer(serializers.ModelSerializer):

    class Meta:
        model = ClientContact
        fields = '__all__'
class ClientSerializer(serializers.ModelSerializer):

    contacts = ClientContactSerializer(many=True, read_only=True, required=False)
    objects = serializers.SerializerMethodField()
    class Meta:
        model = Client
        fields = '__all__'

    def get_objects(self,obj):
        from object.serializers import ClientObjectSerializer
        return ClientObjectSerializer(obj.client_objects, many=True).data






