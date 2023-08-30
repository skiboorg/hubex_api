from django.urls import path,include
from . import views
from .router import router
urlpatterns = [
    path('', include(router.urls)),
    path('equipment_by_object', views.GetByObject.as_view()),
    path('equipment_firm', views.GetFirm.as_view()),
    path('equipment_model', views.GetModel.as_view()),
    path('equipment_update', views.UpdateEquipment.as_view()),

]
