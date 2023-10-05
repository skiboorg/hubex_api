
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




class EquipmentFirmSerializer(serializers.ModelSerializer):

    class Meta:
        model = EquipmentFirm
        fields = '__all__'
class EquipmentGroupSerializer(serializers.ModelSerializer):

    class Meta:
        model = EquipmentGroup
        fields = '__all__'

class EquipmentModelSerializer(serializers.ModelSerializer):
    firm = EquipmentFirmSerializer(many=False, read_only=True, required=False)
    group = EquipmentGroupSerializer(many=False, read_only=True, required=False)
    class Meta:
        model = EquipmentModel
        fields = '__all__'



class EquipmentSerializer(serializers.ModelSerializer):
    from object.serializers import ObjectSerializer
    from order.serializers import OrderShortSerializer
    model = EquipmentModelSerializer(many=False, read_only=True, required=False)
    object = ObjectSerializer(many=False, read_only=True, required=False)
    orders = OrderShortSerializer(many=True, read_only=True, required=False)
    class Meta:
        model = Equipment
        fields = '__all__'

