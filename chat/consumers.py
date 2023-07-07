import json

from channels.generic.websocket import AsyncWebsocketConsumer

from channels.db import database_sync_to_async
from channels.layers import get_channel_layer
from asgiref.sync import async_to_sync
from user.models import User

class UserOnline(AsyncWebsocketConsumer):
    user = None

    async def connect(self):
        print('connect')
        # self.room_name = 'order_chat'
        # self.room_group_name = 'order_chat'
        # await self.channel_layer.group_add(
        #     self.room_group_name,
        #     self.channel_name
        # )
        await self.accept()

    async def disconnect(self, close_code):
        # Leave room group
        # print(self.user)
        await self.channel_layer.group_discard(
            'users',
            self.channel_name
        )
        await self.set_user_offline()

    @database_sync_to_async
    def set_user_offline(self):
        print('disconnect')
        self.user.channel = None
        self.user.is_online = False
        self.user.save(update_fields=["channel",'is_online'])
        return

    @database_sync_to_async
    def get_user(self, uuid):
        print('get_user')
        user = User.objects.get(uuid=uuid)
        print(user)
        return user


    async def receive(self, text_data):
        text_data_json = json.loads(text_data)
        print('receive data', text_data_json)
        self.user = await self.get_user(text_data_json['uuid'])
        await self.channel_layer.group_add("users", self.channel_name)
        print(f"Added {self.channel_name} channel to users")
        await self.save_user_channel()
        # if text_data_json.get('logout_id'):
        #     await self.disconnect(1)

    # async def send(self, text_data):
    #     print(self,text_data)

    @database_sync_to_async
    def save_user_channel(self):
        self.user.channel = self.channel_name
        self.user.is_online = True
        self.user.save(update_fields=["channel", 'is_online'])
        return


    async def user_notify(self, event):
        # Handles the "chat.message" event when it's sent to us.

        message = event['message']
        type = event['event']
        # url = event['url']
        event_id = event['event_id']
        await self.send(text_data=json.dumps({
             'event': type,
             'message': message,
             # 'url': url,
             'event_id': event_id,

         }))
    # async def chat_message(self, event):
    #     message = event['message']
    #
    #     # Send message to WebSocket
    #     await self.send(text_data=json.dumps({
    #         'message': message
    #     }))

class OrderChatConsumer(AsyncWebsocketConsumer):
    async def connect(self):
        # print(self.scope["path"])
        print(self.scope['url_route'])
        self.room_name = self.scope['url_route']['kwargs']['order_uid']
        self.room_group_name = 'chat_%s' % self.room_name
        # print(self.room_name)
        print(self.room_group_name)
        await self.channel_layer.group_add(
            self.room_group_name,
            self.channel_name
        )
        await self.accept()

    async def disconnect(self, close_code):
        await self.channel_layer.group_discard(
            self.room_group_name,
            self.channel_name
        )

    # Receive message from WebSocket
    async def receive(self, text_data):
        text_data_json = json.loads(text_data)
        message = text_data_json['message']

        # Send message to room group
        await self.channel_layer.group_send(
            self.room_group_name,
            {
                'type': 'chat_message',
                'message': message
            }
        )

    # Receive message from room group
    async def chat_message(self, event):
        print('send')
        message = event['message']

        # Send message to WebSocket
        await self.send(text_data=json.dumps({
            'type': 'message',
            'message': message
        }))



