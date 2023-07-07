import json
from decimal import Decimal
from uuid import uuid4
from rest_framework import generics
from rest_framework.views import APIView
from rest_framework.response import Response
from .serializers import *
from itertools import chain
from channels.layers import get_channel_layer
from asgiref.sync import async_to_sync
from .services import send_to_all_users_websocket_notify,send_to_user_websocket_notify
from user.models import User

channel_layer = get_channel_layer()


class GetOrderChat(generics.RetrieveAPIView):
    serializer_class = OrderChatSerializer

    def get_object(self):
        order_uuid = self.request.query_params.get('order')
        print('order_uuid',order_uuid)
        chat = OrderChat.objects.get(order__uuid=order_uuid)
        return chat


class AddMessageInOrderChat(APIView):
    def post(self,request):
        data = request.data
        order_uuid = data['order']
        message = json.loads(data['message'])
        user_uuid = data['user']
        user = User.objects.get(uuid=user_uuid)
        chat = OrderChat.objects.get(order__uuid=order_uuid)

        new_message = OrderChatMessage.objects.create(user=user, chat=chat, message=message)

        for f in request.FILES.getlist('file'):
            new_message.file = f
            new_message.save(update_fields=['file'])

        message = OrderChatMessageSerializer(new_message, many=False)

        async_to_sync(channel_layer.group_send)(f'chat_{chat.order.uuid}',
                                                {"type": "chat.message",
                                                 'message': message.data,
                                                 'chatId': chat.id})

        return Response(status=200)