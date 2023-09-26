
from django.utils import timezone
from datetime import timedelta

from django.contrib.auth import authenticate, get_user_model
from django.contrib.auth.password_validation import validate_password
from django.core import exceptions as django_exceptions
from django.db import IntegrityError, transaction

from rest_framework import exceptions, serializers, status, generics
from .models import *
from djoser.conf import settings

from order.models import Order

from django.contrib.auth.tokens import default_token_generator

# from .services import send_email




import logging
logger = logging.getLogger(__name__)




class PagePermissionSerializer(serializers.ModelSerializer):
    class Meta:
        model = PagePermission
        fields = '__all__'

class UserWorkTimeTypeSerializer(serializers.ModelSerializer):
    class Meta:
        model = UserWorkTimeType
        fields = '__all__'

class PageSerializer(serializers.ModelSerializer):
    class Meta:
        model = Page
        fields = '__all__'

class RolePageSerializer(serializers.ModelSerializer):
    page = PageSerializer(many=False, required=False, read_only=True)
    permission = PagePermissionSerializer(many=False, required=False, read_only=True)
    class Meta:
        model = RolePage
        fields = '__all__'


class RoleSerializer(serializers.ModelSerializer):
    pages = RolePageSerializer(many=True, required=False, read_only=True)
    class Meta:
        model = Role
        fields = '__all__'


class NotificationSerializer(serializers.ModelSerializer):
    class Meta:
        model = Notification
        fields = '__all__'



class UserWorkTimeSerializer(serializers.ModelSerializer):

    title = serializers.SerializerMethodField()
    order_data = serializers.SerializerMethodField()
    type = UserWorkTimeTypeSerializer(many=False, required=False, read_only=True)

    class Meta:
        model = UserWorkTime
        fields = '__all__'
    def get_title(self,obj):
        return f'Заявка {obj.order.number}'
    def get_order_data(self,obj):
        result = {}
        result['order_number'] = obj.order.number
        result['order_created'] = obj.order.date_created_at
        result['equipment_sn'] = obj.order.equipment.serial_number
        result['status_name'] = obj.order.status.name
        result['status_bg_color'] = obj.order.status.bg_color
        result['status_text_color'] = obj.order.status.text_color
        result['stage_name'] = obj.order.stage.name
        result['object_address'] = obj.order.object.address
        result['object_number'] = obj.order.object.number

        return result





class UserSaveSerializer(serializers.ModelSerializer):
    class Meta:
        model = User
        fields = [
            "id",
            'fio',
            "phone",
            "uuid",

        ]

class UserShortSerializer(serializers.ModelSerializer):
    class Meta:
        model = User
        fields = [
            "id",
                "uuid",
                "login",
                "fio",
                "phone",
            'email',
            'role',
            'is_driving',
            'is_staff',
            'avatar',
            'telega',


        ]
class UserSerializer(serializers.ModelSerializer):
    role = RoleSerializer(many=False,required=False,read_only=True)
    work_time = UserWorkTimeSerializer(many=True,required=False,read_only=True)
    notifications = NotificationSerializer(many=True,required=False,read_only=True)
    class Meta:
        model = User
        fields = [
            "id",
                "uuid",
                "login",
                "fio",
                "phone",
            'email',
            'role',
            'is_driving',
            'is_staff',
            'avatar',
            'work_time',
            'notifications',
            'telega',


        ]

        extra_kwargs = {
            'password': {'required': False},

        }


class UserCreateSerializer(serializers.ModelSerializer):
    password = serializers.CharField(style={"input_type": "password"}, write_only=True)

    default_error_messages = {
        "cannot_create_user": settings.CONSTANTS.messages.CANNOT_CREATE_USER_ERROR
    }

    class Meta:
        model = User
        fields = tuple(User.REQUIRED_FIELDS) + (
            'added_by',
            'fio',
            'phone',
            'login',
            'password',
        )

    def validate(self, attrs):
        user = User(**attrs)
        password = attrs.get("password")


        try:
            validate_password(password, user)
        except django_exceptions.ValidationError as e:
            serializer_error = serializers.as_serializer_error(e)
            print(e)
            raise serializers.ValidationError(
                {"password": serializer_error["non_field_errors"]}
            )

        return attrs

    def create(self, validated_data):
        try:
            user = self.perform_create(validated_data)
        except IntegrityError:
            self.fail("cannot_create_user")

        return user

    def perform_create(self, validated_data):

        with transaction.atomic():
            user = User.objects.create_user(**validated_data)
            user.is_active = True
            user.save(update_fields=["is_active"])

        return user


