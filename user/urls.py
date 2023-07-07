from django.urls import path,include
from . import views

urlpatterns = [


    path('me', views.GetUser.as_view()),
    path('my_users', views.GetMyUsers.as_view()),
    path('all', views.GetAllUsers.as_view()),
    path('by_role', views.GetUserByRole.as_view()),
    path('roles', views.GetRoles.as_view()),

    path('add_user', views.AddUser.as_view()),
    path('update_user', views.UpdateUser.as_view()),

    path('get_user/<uuid>', views.GetUserByUuid.as_view()),
    path('delete_user/<uuid>', views.DeleteUser.as_view()),










]
