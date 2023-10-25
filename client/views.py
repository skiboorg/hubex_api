from .serializers import *
from .models import *
from rest_framework import generics, viewsets, parsers
from rest_framework.response import Response

class ClientContactViewSet(viewsets.ModelViewSet):
    queryset = ClientContact.objects.all()
    serializer_class = ClientContactSerializer
class ClientViewSet(viewsets.ModelViewSet):
    queryset = Client.objects.all()
    serializer_class = ClientSerializer

    def create(self, request, *args, **kwargs):
        print(request.data)
        serializer = self.get_serializer(data=request.data['client'])
        if serializer.is_valid():
            obj = serializer.save()
            for c in request.data['contacts']:
                print(c)
                c_serializer = ClientContactSerializer(data=c)
                if c_serializer.is_valid():
                    c_obj = c_serializer.save()
                    c_obj.client = obj
                    c_obj.save()
                else:
                    print(serializer.errors)

        else:
            print(serializer.errors)
        headers = self.get_success_headers(serializer.data)
        return Response(serializer.data, status=status.HTTP_201_CREATED, headers=headers)

    def update(self, request, *args, **kwargs):
        #$print(request.data)
        instance = self.get_object()
        serializer = self.get_serializer(instance, data=request.data['client'])
        if serializer.is_valid():
            obj = serializer.save()
            for c in request.data['contacts']:
                if c.get('id',None):
                    contact = ClientContact.objects.get(id=c['id'])
                    contact_serializer = ClientContactSerializer(instance=contact, data=c)
                    if contact_serializer.is_valid():
                        contact_serializer.save()
                else:
                    b = c.pop('is_new')
                    ClientContact.objects.create(**c)
        else:
            print(serializer.errors)
        headers = self.get_success_headers(serializer.data)
        return Response(serializer.data, status=status.HTTP_200_OK, headers=headers)