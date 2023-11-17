from django.urls import path,include
from . import views

urlpatterns = [
    path('weekly', views.WeeklyStats.as_view()),


]
