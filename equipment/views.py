from rest_framework.views import APIView
from rest_framework.response import Response
from .serializers import *
from .models import *
from rest_framework import generics, viewsets, parsers
from django_filters.rest_framework import DjangoFilterBackend
from rest_framework import filters
import django_filters
from django.db.models import Count, Q
from django_filters import IsoDateTimeFilter

class EquipmentFilter(django_filters.FilterSet):
    date_in_work_gte = IsoDateTimeFilter(field_name="date_in_work", lookup_expr='gte')
    date_in_work_lte = IsoDateTimeFilter(field_name="date_in_work", lookup_expr='lte')

    q = django_filters.CharFilter(method='my_custom_filter', label="Search")

    def my_custom_filter(self, queryset, name, value):
        return queryset.filter(
            Q(serial_number__icontains=value) |
            Q(name__icontains=value) |
            Q(model__firm__name__icontains=value) |
            Q(model__name__icontains=value)
        )

    class Meta:
        model = Equipment
        fields = {
            'is_warranty': ('exact',),
            'is_service_book_sign': ('exact',),
            'model__firm_id': ('exact',),
            'model_id': ('exact',),

        }

class EquipmentViewSet(viewsets.ModelViewSet):
    queryset = Equipment.objects.all()
    serializer_class = EquipmentSerializer
    lookup_field = 'serial_number'
    filter_backends = [DjangoFilterBackend, filters.OrderingFilter]
    filterset_class = EquipmentFilter

    def perform_create(self, serializer):
        print(self.request.data)
        model_id = self.request.data['model']
        object_id = self.request.data['object']
        serializer.save(
            # name=self.request.data['data']['name'],
            model_id=model_id,
            object_id=object_id,
        )

    def perform_update(self, serializer):
        print(self.request.data)
        model_id = self.request.data['model']
        object_id = self.request.data['object']
        serializer.save(
            # name=self.request.data['data']['name'],
            model_id=model_id,
            object_id=object_id,
        )

class GetByObject(generics.ListAPIView):
    serializer_class= EquipmentSerializer

    def get_queryset(self):
        return Equipment.objects.filter(object_id=self.request.query_params.get('obj_id'))

class GetFirm(generics.ListAPIView):
    serializer_class= EquipmentFirmSerializer
    queryset = EquipmentFirm.objects.all()

class GetModel(generics.ListAPIView):
    serializer_class= EquipmentModelSerializer

    def get_queryset(self):
        return EquipmentModel.objects.filter(firm__id=self.request.query_params.get('firm'))


class UpdateEquipment(APIView):
    def post(self, request):
        equipment = Equipment.objects.get(serial_number=self.request.query_params.get('serial'))

        data = request.data
        print(data)

        equipment.firm_id = data['firm']
        equipment.model_id = data['model']
        equipment.object_id = data['object']
        equipment.name = data['name']
        equipment.comment = data['comment']
        equipment.is_warranty = data['is_warranty']
        equipment.is_service_book_sign = data['is_service_book_sign']
        equipment.warranty_ends = data['warranty_ends']
        equipment.service_book_sign_date = data['service_book_sign_date']
        equipment.date_in_work = data['date_in_work']
        equipment.save()


        return Response(status=200)