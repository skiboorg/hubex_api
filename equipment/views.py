from .serializers import *
from .models import *
from rest_framework import generics, viewsets, parsers


class EquipmentViewSet(viewsets.ModelViewSet):
    queryset = Equipment.objects.all()
    serializer_class = EquipmentSerializer
    lookup_field = 'serial_number'