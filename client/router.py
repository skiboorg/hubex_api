from rest_framework import routers
from .views import *
router = routers.SimpleRouter(trailing_slash=False)
router.register(r'client', ClientViewSet)
router.register(r'client_contact', ClientContactViewSet)


