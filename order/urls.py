from django.urls import path,include
from . import views
from .router import router
urlpatterns = [
    path('save_check_list_data', views.SaveCheckListData.as_view()),
    path('', include(router.urls)),



]
