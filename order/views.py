from rest_framework.views import APIView
from rest_framework.response import Response
from .serializers import *
from .models import *
from rest_framework import generics, viewsets, parsers


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

    def perform_update(self, serializer):

        stage_id = self.request.data.get('stage_id', None)
        if stage_id:
            serializer.save(
                stage_id=stage_id
            )
            StageLog.objects.create(user=self.request.user,order=serializer.instance,new_stage_id=stage_id)

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