
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

class ShortEquipmentSerializer(serializers.ModelSerializer):

    class Meta:
        model = Equipment
        fields = '__all__'

class ClientContactSerializer(serializers.ModelSerializer):

    class Meta:
        model = ClientContact
        fields = '__all__'
class ClientSerializer(serializers.ModelSerializer):
    contacts = ClientContactSerializer(many=True, read_only=True, required=False)
    class Meta:
        model = Client
        fields = '__all__'


class ObjectImageSerializer(serializers.ModelSerializer):
    class Meta:
        model = ObjectImage
        fields = '__all__'


class ObjectContactSerializer(serializers.ModelSerializer):
    class Meta:
        model = ObjectContact
        fields = '__all__'




class ObjectSerializer(serializers.ModelSerializer):
    images = ObjectImageSerializer(many=True,read_only=True, required=False)
    contacts = ObjectContactSerializer(many=True, read_only=True, required=False)
    equipments = ShortEquipmentSerializer(many=True, read_only=True, required=False)
    class Meta:
        model = Object
        fields = '__all__'






class OrderTypeSerializer(serializers.ModelSerializer):
    class Meta:
        model = OrderType
        fields = '__all__'


class OrderStatusSerializer(serializers.ModelSerializer):
    class Meta:
        model = OrderStatus
        fields = '__all__'

class OrderWorkTypeSerializer(serializers.ModelSerializer):
    class Meta:
        model = OrderWorkType
        fields = '__all__'



class OrderSerializer(serializers.ModelSerializer):
    type = OrderTypeSerializer(many=False, read_only=True, required=False)
    status = OrderStatusSerializer(many=False, read_only=True, required=False)
    work_type = OrderWorkTypeSerializer(many=False, read_only=True, required=False)
    object = ObjectSerializer(many=False, read_only=True, required=False)
    equipment = ShortEquipmentSerializer(many=False, read_only=True, required=False)
    class Meta:
        model = Order
        fields = '__all__'


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
    object = ObjectSerializer(many=False, read_only=True, required=False)
    orders = OrderSerializer(many=True, read_only=True, required=False)
    class Meta:
        model = Equipment
        fields = '__all__'