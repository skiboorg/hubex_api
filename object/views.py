import json
from rest_framework.response import Response
from .serializers import *
from .models import *
from rest_framework import generics, viewsets, parsers


class ObjectViewSet(viewsets.ModelViewSet):
    queryset = Object.objects.all()
    serializer_class = ObjectSerializer
    lookup_field = 'number'

    def create(self, request, *args, **kwargs):
        print(request.data)
        setattr(request.data, '_mutable', True)

        try:
            request.data.pop('image')
        except:
            pass
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
            obj.client_id = json_data['client']

            image = request.FILES.get('image',None)
            if image:
                obj.image = image
            obj.save()
            for index,file in enumerate(request.FILES.getlist('files')):
                ObjectFile.objects.create(file=file,object=obj,text=files_descriptions[index])

            for contact in json_data['contacts']:
                contact_serializer = ObjectContactSerializer(data=contact)
                if contact_serializer.is_valid():
                    contact_obj = contact_serializer.save()
                    contact_obj.object = obj
                    contact_obj.save()
            for equipment in json_data['equipments']:
                ObjectAdditionalEquipment.objects.create(object=obj,
                                                         model_id=equipment['model'],
                                                         amount=equipment['amount'])
        else:
            print(serializer.errors)

        headers = self.get_success_headers(serializer.data)
        return Response(serializer.data, status=status.HTTP_201_CREATED, headers=headers)


class GetAddEqCategory(generics.ListAPIView):
    serializer_class = AdditionalEquipmentCategorySerializer
    queryset = AdditionalEquipmentCategory.objects.all()

class GetAddEqModel(generics.ListAPIView):
    serializer_class = AdditionalEquipmentModelSerializer


    def get_queryset(self):
        return AdditionalEquipmentModel.objects.filter(category_id=self.request.query_params.get('c_id'))
