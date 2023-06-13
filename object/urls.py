from django.urls import path,include
from . import views
from .router import router
urlpatterns = [
    path('', include(router.urls)),
    # path('rashodnik_categories', views.GetRashodnikCategories.as_view()),

]
