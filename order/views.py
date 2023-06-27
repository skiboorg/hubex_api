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



class OrderFilter(django_filters.FilterSet):
    created_at_gte = IsoDateTimeFilter(field_name="date_created_at", lookup_expr='gte')
    created_at_lte = IsoDateTimeFilter(field_name="date_created_at", lookup_expr='lte')
    class Meta:
        model = Order
        fields = {
            'is_done': ('exact',),
            'is_critical': ('exact',),
        }
class OrderViewSet(viewsets.ModelViewSet):
    queryset = Order.objects.all()
    serializer_class = OrderSerializer
    filter_backends = [DjangoFilterBackend, filters.OrderingFilter]
    lookup_field = 'number'
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
        print(full_mode)
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
            obj.object_id = json_data['object']
            obj.equipment_id = json_data['equipment']
            obj.save()
            for index,file in enumerate(request.FILES.getlist('files')):
                OrderFile.objects.create(file=file,order=obj,text=files_descriptions[index])
        else:
            print(serializer.errors)

        headers = self.get_success_headers(serializer.data)
        return Response(serializer.data, status=status.HTTP_201_CREATED, headers=headers)

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
            serializer.save(is_done=True, stage_id=None, status=done_status)

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