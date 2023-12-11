
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

class WorkTypeSerializer(serializers.ModelSerializer):
    class Meta:
        model = WorkType
        fields = '__all__'

class CheckListTableInputFieldSerializer(serializers.ModelSerializer):
    class Meta:
        model = CheckListTableInputField
        fields = '__all__'


class CheckListTableInputSerializer(serializers.ModelSerializer):
    input = CheckListTableInputFieldSerializer(many=False, read_only=True, required=False)
    class Meta:
        model = CheckListTableInput
        fields = '__all__'
class CheckListTableDataSerializer(serializers.ModelSerializer):
    class Meta:
        model = CheckListTableData
        fields = '__all__'


class CheckListTableSerializer(serializers.ModelSerializer):
    check_list_table_inputs = CheckListTableInputSerializer(many=True, read_only=True, required=False)

    class Meta:
        model = CheckListTable
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
    check_list_tables = CheckListTableSerializer(many=True, read_only=True, required=False)
    class Meta:
        model = CheckList
        fields = '__all__'

class StageGroupSelectSerializer(serializers.ModelSerializer):

    check_list = CheckListSerializer(many=False, read_only=True, required=False)
    #group = serializers.SerializerMethodField()
    class Meta:
        model = StageGroupSelect
        fields = '__all__'

    def get_group(self,obj):
        from equipment.serializers import EquipmentGroupSerializer
        return EquipmentGroupSerializer(obj.equipment_group).data

class StageButtonSerializer(serializers.ModelSerializer):
    class Meta:
        model = StageButton
        fields = '__all__'

class StageSerializer(serializers.ModelSerializer):
    from user.serializers import RoleSerializer
    groups = StageGroupSelectSerializer(many=True, read_only=True, required=False)
    buttons = StageButtonSerializer(many=True, read_only=True, required=False)
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
    from user.serializers import UserShortSerializer
    user = UserShortSerializer(many=False, read_only=True, required=False)
    new_stage = StageShortSerializer(many=False, read_only=True, required=False)
    class Meta:
        model = StageLog
        fields = '__all__'


class CheckListDataSerializer(serializers.ModelSerializer):
    check_list= CheckListSerializer(many=False, read_only=True, required=False)
    order_number = serializers.SerializerMethodField()
    equipment = serializers.SerializerMethodField()
    object = serializers.SerializerMethodField()
    object_add_equipment = serializers.SerializerMethodField()
    class Meta:
        model = CheckListData
        fields = '__all__'

    def get_order_number(self,obj):
        return obj.order.number
    def get_equipment(self,obj):
        from equipment.serializers import EquipmentSerializer
        if obj.order.equipment:
            return EquipmentSerializer(obj.order.equipment, many=False).data


    def get_object(self,obj):
        from object.serializers import ObjectSerializer
        if obj.order.object:

            return ObjectSerializer(obj.order.object, many=False).data
    def get_object_add_equipment(self,obj):
        from object.serializers import ObjectAdditionalEquipmentSerializer
        if obj.order.object:
            print(obj.order.object.additional_equipments.all())
            return ObjectAdditionalEquipmentSerializer(obj.order.object.additional_equipments.all(),many=True).data


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


class EquipmentShortSerializer(serializers.ModelSerializer):

    class Meta:
        model = Equipment
        fields = ['id','serial_number']

class OrderFileSerializer(serializers.ModelSerializer):
    class Meta:
        model = OrderFile
        fields = '__all__'

class OrdersForWorkerSerializer(serializers.ModelSerializer):
    from user.serializers import OrderUserSerializer
    from object.serializers import ObjectShortSerializer

    type = TypeSerializer(many=False, read_only=True, required=False)
    work_type = WorkTypeSerializer(many=False, read_only=True, required=False)
    status = StatusSerializer(many=False, read_only=True, required=False)
    stage = StageShortSerializer(many=False, read_only=True, required=False)
    object = ObjectShortSerializer(many=False, read_only=True, required=False)
    equipment = EquipmentShortSerializer(many=False, read_only=True, required=False)
    users = OrderUserSerializer(many=True, read_only=True, required=False)

    #check_lists = CheckListDataSerializer(many=True, read_only=True, required=False)
    #stage_logs = StageLogSerializer(many=True, read_only=True, required=False)
    files = OrderFileSerializer(many=True, read_only=True, required=False)

    class Meta:
        model = Order
        fields = '__all__'

class OrderSerializer(serializers.ModelSerializer):
    from user.serializers import UserSerializer
    from object.serializers import ObjectSerializer

    type = TypeSerializer(many=False, read_only=True, required=False)
    work_type = WorkTypeSerializer(many=False, read_only=True, required=False)
    status = StatusSerializer(many=False, read_only=True, required=False)
    stage = StageSerializer(many=False, read_only=True, required=False)
    object = ObjectSerializer(many=False, read_only=True, required=False)
    equipment = EquipmentSerializer(many=False, read_only=True, required=False)
    #users = UserSerializer(many=True, read_only=True, required=False)
    users = serializers.SerializerMethodField()
    check_lists = CheckListDataSerializer(many=True, read_only=True, required=False)
    stage_logs = StageLogSerializer(many=True, read_only=True, required=False)
    files = OrderFileSerializer(many=True, read_only=True, required=False)
    class Meta:
        model = Order
        fields = '__all__'

    def get_users(self, obj):
        print ('number',obj.number)
        result = []
        for user in obj.users.all():
            data = {
                "id": None,
                "avatar":None,
                "fio":None,
                "role":{
                    "name":'test'
                },
                "order_data":{
                    "order_number":None
                },
                "work_time":None,
            }


            data['id']=user.id
            data['avatar']=user.avatar if user.avatar else None
            data['fio']=user.fio
            data['role']['name']=user.role.name

            times = []
            for time in user.work_time.all():

                if time.order.number == obj.number:
                    print(time)
                    times.append({
                        'date':time.date,
                        'end_time':time.end_time,
                        'id':time.id,
                        'start_time':time.start_time,
                        'title':f'Заявка {obj.number}',
                        "order_data": {
                            "order_number": obj.number
                        },
                        "type":{
                            "name":time.type.name if time.type else 'Не указано'
                        }
                    })
            data['work_time'] = times
            result.append(data)
        return result


class OrderShortSerializer(serializers.ModelSerializer):
    from object.serializers import ObjectShortSerializer

    status = StatusSerializer(many=False, read_only=True, required=False)
    object = ObjectShortSerializer(many=False, read_only=True, required=False)
    equipment = EquipmentShortSerializer(many=False, read_only=True, required=False)
    type = TypeSerializer(many=False, read_only=True, required=False)
    work_type = WorkTypeSerializer(many=False, read_only=True, required=False)
    class Meta:
        model = Order
        fields = '__all__'
