from django.urls import path,include
from . import views
from .router import router
urlpatterns = [
    path('save_check_list_data', views.SaveCheckListData.as_view()),
    path('order_history_by_object/<int:object_id>', views.GetOrdersHistoryByObject.as_view()),
    path('order_by_worker/<int:id>', views.GetOrdersByWorker.as_view()),
    path('order_by_worker_calendar/<int:id>', views.GetOrdersByWorkerForCalendar.as_view()),
    path('order_by_user/<int:id>', views.GetOrdersByUser.as_view()),
    path('order_add_users', views.AddUsersToOrder.as_view()),
    path('order_add_user', views.AddUserToOrder.as_view()),
    path('order_delete_user', views.DeleteUserFromOrder.as_view()),
    path('order_checklists', views.GetCheckLists.as_view()),
    path('order_checklist', views.GetCheckList.as_view()),
    path('order_types', views.OrderTypes.as_view()),
    path('order_delete_file/<pk>', views.OrderDeleteFile.as_view()),
    path('order_update', views.OrderUpdate.as_view()),
    path('', include(router.urls)),



]
