from .serializers import *
from .models import *
from rest_framework import generics, viewsets, parsers


class EquipmentViewSet(viewsets.ModelViewSet):
    queryset = Equipment.objects.all()
    serializer_class = EquipmentSerializer
    lookup_field = 'serial_number'

    def perform_create(self, serializer):
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