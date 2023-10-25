
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



class ObjectFileSerializer(serializers.ModelSerializer):
    class Meta:
        model = ObjectFile
        fields = '__all__'


class ObjectContactSerializer(serializers.ModelSerializer):
    class Meta:
        model = ObjectContact
        fields = '__all__'


class AdditionalEquipmentCategorySerializer(serializers.ModelSerializer):

    class Meta:
        model = AdditionalEquipmentCategory
        fields = '__all__'


class AdditionalEquipmentModelSerializer(serializers.ModelSerializer):
    category = AdditionalEquipmentCategorySerializer(many=False, required=False, read_only=True)
    class Meta:
        model = AdditionalEquipmentModel
        fields = '__all__'




class ObjectAdditionalEquipmentSerializer(serializers.ModelSerializer):
    model = AdditionalEquipmentModelSerializer(many=False, required=False, read_only=True)
    class Meta:
        model = ObjectAdditionalEquipment
        fields = '__all__'


class ObjectSerializer(serializers.ModelSerializer):
    from client.serializers import ClientSerializer
    files = ObjectFileSerializer(many=True,read_only=True, required=False)
    contacts = ObjectContactSerializer(many=True, read_only=True, required=False)
    client = ClientSerializer(many=False, required=False, read_only=True)
    additional_equipments = ObjectAdditionalEquipmentSerializer(many=True, required=False, read_only=True)
    class Meta:
        model = Object
        fields = '__all__'

class ClientObjectSerializer(serializers.ModelSerializer):

    class Meta:
        model = Object
        fields = '__all__'




