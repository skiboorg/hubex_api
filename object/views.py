from .serializers import *
from .models import *
from rest_framework import generics, viewsets, parsers


class ObjectViewSet(viewsets.ModelViewSet):
    queryset = Object.objects.all()
    serializer_class = ObjectSerializer
    lookup_field = 'number'
