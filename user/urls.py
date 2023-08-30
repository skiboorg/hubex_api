from django.urls import path,include
from . import views

urlpatterns = [


    path('me', views.GetUser.as_view()),
    path('my_users', views.GetMyUsers.as_view()),
    path('all', views.GetAllUsers.as_view()),
    path('by_role', views.GetUserByRole.as_view()),
    path('roles', views.GetRoles.as_view()),
    path('time_types', views.GetTimeTypes.as_view()),
    path('find_by_work_time', views.FindByWorkTime.as_view()),
    path('find_worker_time_for_calendar', views.GetOrdersByWorkerForCalendar.as_view()),
    path('get_work_events', views.GetWorkEvents.as_view()),

    path('add_user', views.AddUser.as_view()),
    path('update_user', views.UpdateUser.as_view()),
    path('hide_time', views.HideUnhideTime.as_view()),

    path('get_user/<uuid>', views.GetUserByUuid.as_view()),
    path('delete_user/<uuid>', views.DeleteUser.as_view()),
    path('update_user_work_time', views.UpdateUserWorkTime.as_view()),
    path('set_notify_read', views.SetNotifyRead.as_view()),
    path('del_notify', views.DelNotify.as_view()),










]
