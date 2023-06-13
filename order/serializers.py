
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



class StatusSerializer(serializers.ModelSerializer):
    class Meta:
        model = Status
        fields = '__all__'

class InputFieldSerializer(serializers.ModelSerializer):
    class Meta:
        model = InputField
        fields = '__all__'


class CheckListInputSerializer(serializers.ModelSerializer):
    input = InputFieldSerializer(many=False, read_only=True, required=False)
    class Meta:
        model = CheckListInput
        fields = '__all__'


class CheckListSerializer(serializers.ModelSerializer):
    inputs = CheckListInputSerializer(many=True, read_only=True, required=False)
    class Meta:
        model = CheckList
        fields = '__all__'


class StageSerializer(serializers.ModelSerializer):
    check_list = CheckListSerializer(many=False, read_only=True, required=False)
    class Meta:
        model = Stage
        fields = '__all__'


class CheckListDataSerializer(serializers.ModelSerializer):
    class Meta:
        model = CheckListData
        fields = '__all__'



class OrderSerializer(serializers.ModelSerializer):
    from object.serializers import ObjectSerializer
    from equipment.serializers import EquipmentSerializer
    status = StatusSerializer(many=False, read_only=True, required=False)
    stage = StageSerializer(many=False, read_only=True, required=False)
    object = ObjectSerializer(many=False, read_only=True, required=False)
    equipment = EquipmentSerializer(many=False, read_only=True, required=False)
    class Meta:
        model = Order
        fields = '__all__'


