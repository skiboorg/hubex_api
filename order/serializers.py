
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

class TypeSerializer(serializers.ModelSerializer):
    class Meta:
        model = Type
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
    from user.serializers import RoleSerializer
    check_list = CheckListSerializer(many=False, read_only=True, required=False)
    add_user_role = RoleSerializer(many=False, read_only=True, required=False)
    class Meta:
        model = Stage
        fields = '__all__'

class StageShortSerializer(serializers.ModelSerializer):
    class Meta:
        model = Stage
        fields = ['name']

class StageLogSerializer(serializers.ModelSerializer):
    from user.serializers import UserSerializer
    user = UserSerializer(many=False, read_only=True, required=False)
    new_stage = StageShortSerializer(many=False, read_only=True, required=False)
    class Meta:
        model = StageLog
        fields = '__all__'


class CheckListDataSerializer(serializers.ModelSerializer):
    check_list= CheckListSerializer(many=False, read_only=True, required=False)
    order_number = serializers.SerializerMethodField()
    class Meta:
        model = CheckListData
        fields = '__all__'

    def get_order_number(self,obj):
        return obj.order.number

class CheckListDataShortSerializer(serializers.ModelSerializer):
    order_number = serializers.SerializerMethodField()
    check_list_name = serializers.SerializerMethodField()

    def get_order_number(self,obj):
        return obj.order.number

    def get_check_list_name(self,obj):
        return obj.check_list.name
    class Meta:
        model = CheckListData

        exclude = ['data']

class OrderShortSerializer(serializers.ModelSerializer):
    status = StatusSerializer(many=False, read_only=True, required=False)
    stage = StageShortSerializer(many=False, read_only=True, required=False)

    class Meta:
        model = Order
        fields = '__all__'


from equipment.models import *
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
    class Meta:
        model = Equipment
        fields = '__all__'

class OrderFileSerializer(serializers.ModelSerializer):
    class Meta:
        model = OrderFile
        fields = '__all__'

class OrderSerializer(serializers.ModelSerializer):
    from user.serializers import UserSerializer
    from object.serializers import ObjectSerializer

    type = TypeSerializer(many=False, read_only=True, required=False)
    status = StatusSerializer(many=False, read_only=True, required=False)
    stage = StageSerializer(many=False, read_only=True, required=False)
    object = ObjectSerializer(many=False, read_only=True, required=False)
    equipment = EquipmentSerializer(many=False, read_only=True, required=False)
    users = UserSerializer(many=True, read_only=True, required=False)
    check_lists = CheckListDataSerializer(many=True, read_only=True, required=False)
    stage_logs = StageLogSerializer(many=True, read_only=True, required=False)
    files = OrderFileSerializer(many=True, read_only=True, required=False)
    class Meta:
        model = Order
        fields = '__all__'

class OrderShortSerializer(serializers.ModelSerializer):
    from object.serializers import ObjectSerializer

    status = StatusSerializer(many=False, read_only=True, required=False)
    object = ObjectSerializer(many=False, read_only=True, required=False)
    equipment = EquipmentSerializer(many=False, read_only=True, required=False)

    class Meta:
        model = Order
        fields = '__all__'
