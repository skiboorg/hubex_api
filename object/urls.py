from django.urls import path,include
from . import views
from .router import router
urlpatterns = [
    path('', include(router.urls)),

    path('object_equipment_category', views.GetAddEqCategory.as_view()),
    path('object_equipment_model', views.GetAddEqModel.as_view()),

]
