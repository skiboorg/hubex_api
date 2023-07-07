from django.urls import path

from . import consumers

websocket_urlpatterns = [
    path('ws/user/online', consumers.UserOnline.as_asgi()),
    path('ws/order_chat/<order_uid>', consumers.OrderChatConsumer.as_asgi()),
]