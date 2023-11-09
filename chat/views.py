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
from user.models import User,Notification

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
        print(data)
        order_uuid = data['order']
        message = json.loads(data['message'])
        user_uuid = data['user']
        user = User.objects.get(uuid=user_uuid)
        chat = OrderChat.objects.get(order__uuid=order_uuid)
        print(user)
        for userr in chat.users.all():
            if userr != request.user:
                Notification.objects.create(
                    order_number=chat.order.number,
                    user = userr,
                    text = f'Сообщение в чате заявка №{chat.order.number}',
                    link= f'/service/order/{chat.order.number}'
                )

        new_message = OrderChatMessage.objects.create(user=user, chat=chat, message=message)

        for f in request.FILES.getlist('file'):
            new_message.file = f
            new_message.file_name = data['file_name'] if data['file_name'] != 'null' else None
            new_message.save(update_fields=['file','file_name'])

        message = OrderChatMessageSerializer(new_message, many=False)

        async_to_sync(channel_layer.group_send)(f'chat_{chat.order.uuid}',
                                                {"type": "chat.message",
                                                 'message': message.data,
                                                 'chatId': chat.id})

        return Response(status=200)