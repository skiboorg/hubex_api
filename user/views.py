import json

from rest_framework.response import Response
from rest_framework.views import APIView
from rest_framework.permissions import IsAuthenticated
from .serializers import *
from .models import *
from rest_framework import generics, viewsets, parsers


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



class DeleteUser(generics.DestroyAPIView):
    queryset = User.objects.all()
    serializer_class = UserSerializer
    lookup_field = 'uuid'


class GetAllUsers(generics.ListAPIView):
    # permission_classes = [IsAuthenticated]
    serializer_class = UserSerializer
    queryset = User.objects.filter(is_active=True)

class GetRoles(generics.ListCreateAPIView):
    # permission_classes = [IsAuthenticated]
    serializer_class = RoleSerializer
    queryset = Role.objects.all()

