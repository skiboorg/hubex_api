from django.urls import path,include
from . import views
from .router import router
urlpatterns = [
    path('', include(router.urls)),

    path('object_equipment_category', views.GetAddEqCategory.as_view()),
    path('object_equipment_model', views.GetAddEqModel.as_view()),
    path('object_delete_add_equip', views.DeleteAddEq.as_view()),
    path('object_delete_file', views.DeleteFile.as_view()),
    path('object_delete_contact', views.DeleteContact.as_view()),
    path('object_fill', views.FillObject.as_view()),
    path('object_update', views.ObjectUpdate.as_view()),

]
