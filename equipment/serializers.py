
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



class EquipmentModelSerializer(serializers.ModelSerializer):
    class Meta:
        model = EquipmentModel
        fields = '__all__'

class EquipmentFirmSerializer(serializers.ModelSerializer):
    class Meta:
        model = EquipmentFirm
        fields = '__all__'


class EquipmentSerializer(serializers.ModelSerializer):
    model = EquipmentModelSerializer(many=False, read_only=True, required=False)
    firm = EquipmentFirmSerializer(many=False, read_only=True, required=False)
    object = serializers.SerializerMethodField()
    orders = serializers.SerializerMethodField()
    class Meta:
        model = Equipment
        fields = '__all__'

    def get_object(self, obj):
        from object.serializers import ObjectSerializer
        return ObjectSerializer(obj).data

    def get_orders(self, obj):
        from order.serializers import OrderSerializer
        return OrderSerializer(obj).data