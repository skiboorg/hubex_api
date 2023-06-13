from .serializers import *
from .models import *
from rest_framework import generics, viewsets, parsers

class ClientViewSet(viewsets.ModelViewSet):
    queryset = Client.objects.all()
    serializer_class = ClientSerializer