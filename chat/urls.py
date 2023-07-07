from django.urls import path,include
from . import views

urlpatterns = [
    path('get_order_chat', views.GetOrderChat.as_view()),
    path('add_message_in_order_chat', views.AddMessageInOrderChat.as_view()),
]
