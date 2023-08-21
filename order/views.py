import json

from rest_framework.views import APIView
from rest_framework.response import Response
from .serializers import *
from .models import *
from rest_framework import generics, viewsets, parsers
import django_filters
from django_filters import IsoDateTimeFilter
from django_filters.rest_framework import DjangoFilterBackend
from rest_framework import filters
from chat.models import OrderChat
from user.models import User, UserWorkTime
from django.db.models import Count, Q
import datetime

class OrderFilter(django_filters.FilterSet):
    created_at_gte = IsoDateTimeFilter(field_name="date_created_at", lookup_expr='gte')
    created_at_lte = IsoDateTimeFilter(field_name="date_created_at", lookup_expr='lte')
    q = django_filters.CharFilter(method='my_custom_filter', label="Search")

    def my_custom_filter(self, queryset, name, value):
        return queryset.filter(
            Q(number__icontains=value) |
            Q(object__name__icontains=value) |
            Q(equipment__model__name__icontains=value) |
            Q(equipment__serial_number__icontains=value)
        )

    class Meta:
        model = Order
        fields = {
            'is_done': ('exact',),
            'is_critical': ('exact',),
        }
class OrderViewSet(viewsets.ModelViewSet):
    queryset = Order.objects.all()
    serializer_class = OrderSerializer
    lookup_field = 'number'
    filter_backends = [DjangoFilterBackend, filters.OrderingFilter]
    filterset_class = OrderFilter
    # filterset_fields = [
    #     'is_critical',
    #     'is_done',
    #     'created_at_gte',
    #     'created_at_lte',
    # ]

    # def perform_create(self, serializer):
    #     print('serializer.validated_data',serializer.validated_data)
    #     serializer.save()

    def get_serializer_class(self):
        full_mode = self.request.query_params.get('full', None)

        if full_mode:
            return OrderSerializer
        else:
            return OrderShortSerializer

    def create(self, request, *args, **kwargs):

        print(request.data)
        setattr(request.data, '_mutable', True)
        try:
            request.data.pop('files')
            files_descriptions = request.data.pop('descriptions')
        except:
            files_descriptions = []
        data = json.loads(json.dumps(request.data))
        json_data = {}
        for dat in data:
            json_data[dat] = json.loads(data[dat])
        serializer = self.get_serializer(data=json_data)
        if serializer.is_valid():
            obj = serializer.save()
            type_id = json_data.get('type', None)
            if type_id:
                obj.type_id = json_data.get('type',None)

            obj.object_id = json_data['object']
            obj.equipment_id = json_data['equipment']
            if json_data['is_critical']:
                delta = 7
            else:
                delta = 14
            obj.date_dead_line = (datetime.datetime.now() + datetime.timedelta(days=delta)).date()
            obj.save()
            for index,file in enumerate(request.FILES.getlist('files')):
                OrderFile.objects.create(file=file,order=obj,text=files_descriptions[index])
            OrderChat.objects.create(order=obj)
        else:
            print(serializer.errors)

        headers = self.get_success_headers(serializer.data)
        return Response(serializer.data, status=status.HTTP_201_CREATED, headers=headers)

    # def update(self, request, *args, **kwargs):
    #     print(self.request.data)

    def perform_update(self, serializer):
        stage_id = self.request.data.get('stage_id', None)
        is_done = self.request.data.get('is_done', None)

        if stage_id:
            new_stage = Stage.objects.get(id=stage_id)
            if new_stage.status:
                serializer.save(stage_id=stage_id, status=new_stage.status)
            else:
                serializer.save(stage_id=stage_id)

            StageLog.objects.create(user=self.request.user,order=serializer.instance,new_stage=new_stage)

        if is_done:
            done_status = Status.objects.get(is_done=True)
            serializer.save(is_done=True, stage_id=None, status=done_status, date_done=(datetime.datetime.now()).date())

class SaveCheckListData(APIView):
    def post(self, request):
        print(request.data)
        obj,created = CheckListData.objects.get_or_create(order_id=request.data['order_id'],check_list_id=request.data['check_list_id'])

        obj.data = request.data['data']
        obj.save()
        return Response(status=200)

class GetOrdersByWorker(generics.ListAPIView):
    serializer_class = OrderSerializer

    def get_queryset(self):
        user = self.request.user
        print(user.role.id)
        return Order.objects.filter(users__in=[user.id], stage__role_id=user.role.id)

class GetOrdersByWorkerForCalendar(generics.ListAPIView):
    serializer_class = OrderSerializer

    def get_queryset(self):
        user = self.request.user
        print(user.role.id)
        return Order.objects.filter(users__in=[user.id])
class GetOrdersHistoryByObject(generics.ListAPIView):
    serializer_class = OrderSerializer

    def get_queryset(self):
        return Order.objects.filter(object_id=self.kwargs.get('object_id'), is_done=True)


class GetOrdersByUser(generics.ListAPIView):
    serializer_class = OrderSerializer

    def get_queryset(self):
        print(self.kwargs.get('id'))
        return Order.objects.filter(users__in=[self.kwargs.get('id')])


class DeleteUserFromOrder(APIView):
    def post(self, request):
        order_uuid = request.data['order']
        user_uuid = request.data['user']
        order = Order.objects.get(uuid=order_uuid)
        user = User.objects.get(uuid=user_uuid)
        qs = UserWorkTime.objects.filter(order=order, user=user)
        order.users.remove(user)
        if qs.exists():
            qs.first().delete()
        return Response(status=200)



class AddUsersToOrder(APIView):

    def post(self, request):
        order_uuid = request.data['order']
        order_users = request.data['users']
        order = Order.objects.get(uuid=order_uuid)
        chat, _ = OrderChat.objects.get_or_create(order=order)
        print(request.data)

        staff_users = User.objects.filter(is_staff=True)
        for staff_user in staff_users:
            chat.users.add(staff_user)

        for order_user in order_users:
            user = User.objects.get(id=order_user['id'])
            order.users.add(user)
            chat.users.add(user)
            if order_user['events']:
                UserWorkTime.objects.create(
                    user=user,
                    order=order,
                    type_id=order_user['events']['type'],
                    date = order_user['events']['date'].replace('/','-'),
                    start_time=order_user['events']['start_time'],
                    end_time=order_user['events']['end_time'],
                )
            print(order_user)
        return Response(status=200)

class AddUserToOrder(APIView):
    def post(self, request):
        print(request.data)
        order_uuid = request.data['order']
        order_user = request.data['user']
        order = Order.objects.get(uuid=order_uuid)
        chat, _ = OrderChat.objects.get_or_create(order=order)
        user = User.objects.get(uuid=order_user)
        order.users.add(user)
        chat.users.add(user)
        return Response(status=200)

class CheckListFilter(django_filters.FilterSet):

    q = django_filters.CharFilter(method='my_custom_filter', label="Search")

    def my_custom_filter(self, queryset, name, value):
        return queryset.filter(
            Q(check_list__name__icontains=value) |
            Q(order__number__icontains=value)
        )

    class Meta:
        model = CheckListData
        fields = ['created_at']
class GetCheckLists(generics.ListAPIView):
    serializer_class = CheckListDataShortSerializer
    queryset = CheckListData.objects.all()
    filter_backends = [DjangoFilterBackend, filters.OrderingFilter]
    filterset_class = CheckListFilter

class GetCheckList(generics.RetrieveAPIView):
    serializer_class = CheckListDataSerializer
    def get_object(self):
        return CheckListData.objects.get(id=self.request.query_params.get('id'))


class OrderTypes(generics.ListAPIView):
    serializer_class = TypeSerializer
    queryset = Type.objects.all()

class OrderDeleteFile(generics.DestroyAPIView):
    serializer_class = OrderFile
    queryset = OrderFile.objects.all()

class OrderUpdate(APIView):
    def post(self, request):
        order = Order.objects.get(number=self.request.query_params.get('number'))
        print(request.data)
        setattr(request.data, '_mutable', True)

        try:
            request.data.pop('files')
            files_descriptions = request.data.pop('descriptions')
        except:
            files_descriptions = []
        data = json.loads(json.dumps(request.data))
        json_data = {}
        for dat in data:
            json_data[dat] = json.loads(data[dat])
        print(json_data)
        order.object_id = json_data['object']
        order.equipment_id = json_data['equipment']
        order.type_id = json_data['type']
        order.is_critical = json_data['is_critical']
        order.comment = json_data['comment']
        order.date_dead_line = json_data['date_dead_line']
        order.save()
        for index, file in enumerate(request.FILES.getlist('files')):
            OrderFile.objects.create(file=file, order=order, text=files_descriptions[index])

        return Response(status=200)


