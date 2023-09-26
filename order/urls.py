from django.urls import path,include
from . import views
from .router import router
urlpatterns = [
    path('save_check_list_data', views.SaveCheckListData.as_view()),
    path('order_history_by_object/<int:object_id>', views.GetOrdersHistoryByObject.as_view()),
    path('order_by_worker/<int:id>', views.GetOrdersByWorker.as_view()),
    path('order_by_worker_calendar', views.GetOrdersByWorkerForCalendar.as_view()),
    path('order_by_user/<int:id>', views.GetOrdersByUser.as_view()),
    path('order_add_users', views.AddUsersToOrder.as_view()),
    path('order_add_user', views.AddUserToOrder.as_view()),
    path('order_delete_user', views.DeleteUserFromOrder.as_view()),
    path('order_checklists', views.GetCheckLists.as_view()),
    path('order_checklist', views.GetCheckList.as_view()),
    path('order_types', views.OrderTypes.as_view()),
    path('order_work_types', views.OrderWorkTypes.as_view()),
    path('order_delete_file/<pk>', views.OrderDeleteFile.as_view()),
    path('order_update', views.OrderUpdate.as_view()),
    path('order_save_table', views.OrderSaveTable.as_view()),
    path('order_get_table_data', views.OrderGetTableData.as_view()),
    path('order_get_checklist_inputs', views.OrderGetChecklistInputs.as_view()),
    path('order_get_checklist_table_inputs', views.OrderGetChecklistTableInputs.as_view()),
    path('order_create_checklist', views.OrderCreateChecklist.as_view()),
    path('order_update_checklist', views.OrderUpdateChecklist.as_view()),
    path('', include(router.urls)),



]
