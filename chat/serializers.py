from rest_framework import serializers
from .models import *


# class TradeChatUserSerializer(serializers.ModelSerializer):
#     class Meta:
#         model = P2PUser
#         fields = '__all__'

class OrderChatMessageSerializer(serializers.ModelSerializer):
    from user.serializers import UserShortSerializer
    user = UserShortSerializer(many=False, required=False, read_only=True)
    class Meta:
        model = OrderChatMessage
        fields = '__all__'


class OrderChatSerializer(serializers.ModelSerializer):
    messages = OrderChatMessageSerializer(many=True, required=False, read_only=True)
    class Meta:
        model = OrderChat
        fields = [
            'id',
            'messages'
        ]