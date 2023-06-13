from django.contrib import admin
from django.urls import path,include
from django.conf import settings
from django.conf.urls.static import static


urlpatterns = [

    path('admin/', admin.site.urls),
    path('api-auth/', include('rest_framework.urls')),

    path('api/user/', include('user.urls')),
    path('api/data/', include('client.urls')),
    path('api/data/', include('order.urls')),

    path('api/data/', include('object.urls')),
    path('api/data/', include('equipment.urls')),
    # path('api/data/', include(data_router.urls)),

    path('ckeditor/', include('ckeditor_uploader.urls')),

    path('auth/', include('djoser.urls')),
    path('auth/', include('djoser.urls.authtoken')),


] + static(settings.MEDIA_URL, document_root=settings.MEDIA_ROOT)