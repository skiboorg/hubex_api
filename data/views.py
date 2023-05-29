import json

import django_filters
from django_filters import IsoDateTimeFilter
from django_filters.rest_framework import DjangoFilterBackend
from rest_framework import filters
from rest_framework.response import Response
from rest_framework.views import APIView

from .serializers import *
from .models import *
from rest_framework import generics, viewsets, parsers

from PIL import Image, ImageDraw, ImageFont


class OrderViewSet(viewsets.ModelViewSet):
    queryset = Order.objects.all()
    serializer_class = OrderSerializer
    lookup_field = 'number'

    # def perform_create(self, serializer):
    #     print(self.request.data)
    #     type_id = self.request.data['type']['id']
    #     condition_id = self.request.data['condition']['id']
    #     status_id = self.request.data['status']['id']
    #     supplier_id = self.request.data['supplier']['id']
    #     analizes = self.request.data['analizes']
    #     serializer.save(
    #         type_id=type_id,
    #         condition_id=condition_id,
    #         status_id=status_id,
    #         supplier_id=supplier_id,
    #     )

class EquipmentViewSet(viewsets.ModelViewSet):
    queryset = Equipment.objects.all()
    serializer_class = EquipmentSerializer
    lookup_field = 'serial_number'

    # def create(self, request, *args, **kwargs):
    #     setattr(request.data, '_mutable', True)
    #     print(request.FILES)
    #     try:
    #         request.data.pop('image')
    #     except:
    #         pass
    #     data = json.loads(json.dumps(request.data))
    #     json_data = {}
    #     for dat in data:
    #         json_data[dat] = json.loads(data[dat])
    #     serializer = self.get_serializer(data=json_data)
    #     if serializer.is_valid():
    #         obj = serializer.save()
    #         if request.FILES:
    #             print(request.FILES)
    #             obj.image = request.FILES.get('image')
    #             obj.save()
    #
    #     else:
    #         print(serializer.errors)
    #
    #     headers = self.get_success_headers(serializer.data)
    #     return Response(serializer.data, status=status.HTTP_201_CREATED, headers=headers)



class ObjectViewSet(viewsets.ModelViewSet):
    queryset = Object.objects.all()
    serializer_class = ObjectSerializer
    lookup_field = 'number'

    # def perform_create(self, serializer):
    #     item_id = self.request.data['item']['id']
    #     serializer.save(item_id=item_id)


class ClientViewSet(viewsets.ModelViewSet):
    queryset = Client.objects.all()
    serializer_class = ClientSerializer

    # def create(self, request, *args, **kwargs):
    #     setattr(request.data, '_mutable', True)
    #     print(request.FILES)
    #     try:
    #         request.data.pop('image')
    #     except:
    #         pass
    #     data = json.loads(json.dumps(request.data))
    #     json_data = {}
    #     for dat in data:
    #         json_data[dat] = json.loads(data[dat])
    #     serializer = self.get_serializer(data=json_data)
    #     if serializer.is_valid():
    #         obj = serializer.save()
    #         if request.FILES:
    #             print(request.FILES)
    #             obj.image = request.FILES.get('image')
    #             obj.save()
    #
    #     else:
    #         print(serializer.errors)
    #
    #     headers = self.get_success_headers(serializer.data)
    #     return Response(serializer.data, status=status.HTTP_201_CREATED, headers=headers)

