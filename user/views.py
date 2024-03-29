import json

from rest_framework.response import Response
from rest_framework.views import APIView
from rest_framework.permissions import IsAuthenticated
from .serializers import *
from .models import *
from rest_framework import generics, viewsets, parsers
from .services import send_tg_mgs


import logging
logger = logging.getLogger(__name__)



class GetUser(generics.RetrieveAPIView):
    permission_classes = [IsAuthenticated]
    serializer_class = UserSerializer

    def get_object(self):
        return self.request.user


class AddUser(APIView):
    def post(self,request):
        print(request.data)
        setattr(request.data, '_mutable', True)
        try:
            request.data.pop('avatar')
        except:
            pass
        try:
            request.data.pop('files')
            files_descriptions = request.data.pop('descriptions')
        except:
            files_descriptions = []
        try:
            user_networks = request.data.pop('networks')
        except:
            user_networks = []


        data = json.loads(json.dumps(request.data))
        json_data = {}

        for dat in data:
            print(dat)
            json_data[dat] = json.loads(data[dat])
        serializer = UserSerializer(data=json_data)
        avatar = request.FILES.get('avatar', None)
        if serializer.is_valid():
            obj = serializer.save()
            # obj.added_by = request.user
            print(obj)
            if avatar:
                obj.avatar = avatar
            obj.plain_password = json_data['password']
            obj.role_id = json_data['role']
            obj.set_password(json_data['password'])
            obj.save()
            # for index,file in enumerate(request.FILES.getlist('files')):
            #     UserFile.objects.create(file=file,user=obj,description=files_descriptions[index])
            # for network in user_networks:
            #     network_json_data = json.loads(network)
            #     print(network_json_data)
            #     UserNetwork.objects.create(user=obj,network_id=network_json_data['id']['id'],link=network_json_data['link'])

        else:
            print(serializer.errors)
            return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)
        return Response(status=status.HTTP_201_CREATED)


class HideUnhideTime(APIView):
    def get(self, request ):
        print(self.request.query_params.get('id'))
        time = UserWorkTime.objects.get(id=self.request.query_params.get('id'))
        if time.is_hidden:
            time.is_hidden = False
        else:
            time.is_hidden = True
        time.save()
        return Response(status=200)
class UpdateUser(APIView):
    def post(self,request,*args,**kwargs):
        print(request.data)
        setattr(request.data, '_mutable', True)
        try:
            request.data.pop('files')
            files_descriptions = request.data.pop('descriptions')
        except:
            files_descriptions = []
        # try:
        #     user_networks = request.data.pop('networks')
        # except:
        #     user_networks = []


        data = json.loads(json.dumps(request.data))



        json_data = {}
        for dat in data:
            json_data[dat] = json.loads(data[dat])
        instance = User.objects.get(uuid=json_data['uuid'])


        serializer = UserSerializer(instance,data=json_data)

        if serializer.is_valid():
            obj = serializer.save()
            obj.added_by = request.user
            obj.save()
            # for index,file in enumerate(request.FILES.getlist('files')):
            #     UserFile.objects.create(file=file,user=obj,description=files_descriptions[index])
            #
            # for network in user_networks:
            #     network_json_data = json.loads(network)
            #     print(network_json_data)
            #
            #     UserNetwork.objects.create(user=obj,name=network_json_data['name'],link=network_json_data['link'])

        else:
            print(serializer.errors)
            return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)
        return Response(status=status.HTTP_201_CREATED)

class GetMyUsers(generics.ListAPIView):
    serializer_class = UserSerializer

    def get_queryset(self):
        user = User.objects.get(uuid=self.request.query_params.get('id'))
        return User.objects.filter(added_by=user)


class GetUserByUuid(generics.RetrieveAPIView):
    queryset = User.objects.all()
    serializer_class = UserSerializer
    lookup_field = 'uuid'


class GetUserWT(generics.ListAPIView):
    serializer_class = UserWorkTimeSerializer
    def get_queryset(self):
        return UserWorkTime.objects.filter(user_id=self.request.query_params.get('id'))




class DeleteUser(generics.DestroyAPIView):
    queryset = User.objects.all()
    serializer_class = UserSerializer
    lookup_field = 'uuid'


class GetAllUsers(generics.ListAPIView):
    # permission_classes = [IsAuthenticated]
    serializer_class = OrderUserSerializer
    queryset = User.objects.filter(is_active=True)

class GetRoles(generics.ListCreateAPIView):
    # permission_classes = [IsAuthenticated]
    serializer_class = RoleSerializer
    queryset = Role.objects.all()
class GetTimeTypes(generics.ListCreateAPIView):
    # permission_classes = [IsAuthenticated]
    serializer_class = UserWorkTimeTypeSerializer
    queryset = UserWorkTimeType.objects.all()

class GetUserByRole(generics.ListAPIView):
    # permission_classes = [IsAuthenticated]
    serializer_class = UserSerializer
    def get_queryset(self):
        return User.objects.filter(role__id = self.request.query_params.get('id'))

class FindByWorkTime(APIView):
    def get(self, request):
        orders=[]
        result = [
            # {
            #     "order_id": 0,
            #     "work_times":[]
            # },
            # {
            #     "order_id": 24,
            #     "work_times": []
            # },

        ]
        work_time = UserWorkTime.objects.filter(date=self.request.query_params.get('date'))
        for item in work_time:
            if not item.order.id in orders:
                orders.append(item.order.id)
                result.append(
                    {
                        "order_id": item.order.id,
                        'order_number': item.order.number,
                        'order_created': item.order.date_created_at,
                        'equipment_sn': item.order.equipment.serial_number if item.order.equipment else 'Оборудование не указано',
                        'status_name': item.order.status.name,
                        'status_bg_color': item.order.status.bg_color,
                        'status_text_color': item.order.status.text_color,
                        'stage_name': item.order.stage.name,
                        'object_address': item.order.object.address,
                        'object_number': item.order.object.number,
                        "work_times": []
                    },
                )

        for item in work_time:
            print(item)
            for result_item in result:
                if result_item['order_id'] == item.order.id:
                    result_item['work_times'].append({
                        'order_id': item.order.id,
                        'order_number': item.order.number,

                        'user_fio': item.user.fio,
                        'user_role': item.user.role.name,
                        'time_type': item.type.name if item.type else 'Тип времени не указан',
                        'date':item.date,
                        'start_time':item.start_time,
                        'end_time':item.end_time,
                    })

        print(result)
        return Response({'result':result},status=200)


class GetOrdersByWorkerForCalendar(APIView):

    def get(self,request):
        user_id = self.request.query_params.get('user_id')
        date = self.request.query_params.get('date').replace('/','-')
        print(user_id)
        print(date)
        work_times = UserWorkTime.objects.filter(user_id=user_id,date=date)
        print(work_times)
        result = []
        for work_time in work_times:
            result.append(UserWorkTimeSerializer(work_time).data)
        return Response({'result':result}, status=200)

class GetWorkEvents(APIView):
    def get(self, request):
        events = []
        work_time = UserWorkTime.objects.all()
        for item in work_time:
            if item.date:
                print(item.date)
                date = str(item.date).replace('-', '/')
                if not date in events:
                    events.append(date)
        return Response({'events': events}, status=200)

class DelNotify(APIView):
    def get(self, request):
        n_id = self.request.query_params.get('n_id', None)
        if n_id:
            notification = Notification.objects.get(id=n_id)
            notification.delete()
        return Response(status=200)

class UpdateUserWorkTime(APIView):
    def post(self,request):
        data = request.data

        work_times = data['work_time']
        user = None
        order_num = None
        for work_time in work_times:
            user_work_time = UserWorkTime.objects.get(id=work_time['id'])
            if not user:
                user = user_work_time.user
                order_num = user_work_time.order.number
            user_work_time.start_time = work_time['start_time']
            user_work_time.end_time = work_time['end_time']
            user_work_time.save()
        send_tg_mgs(user.telega_id,f'Время выезда изменено по заявке {order_num}')
        return Response(status=200)
class SetNotifyRead(APIView):
    def get(self,request):
        order_num = self.request.query_params.get('o_n', None)
        if order_num:
            notifications = Notification.objects.filter(order_number=order_num)
            notifications.update(is_new=False)

        return Response(status=200)


