from django.urls import path,include
from . import views
from .router import router
urlpatterns = [
    path('', include(router.urls)),
    # path('rashodnik_categories', views.GetRashodnikCategories.as_view()),
    # path('rashodnik_suppliers', views.GetRashodnikSuppliers.as_view()),
    # path('items', views.GetItems.as_view()),
    # path('sample_data', views.GetSampleData.as_view()),
    # path('add_proverka', views.AddProverka.as_view()),



]
