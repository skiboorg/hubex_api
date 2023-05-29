from rest_framework import routers
from .views import *

router = routers.SimpleRouter(trailing_slash=False)
router.register(r'order', OrderViewSet)
router.register(r'equipment', EquipmentViewSet)
router.register(r'object', ObjectViewSet)
router.register(r'client', ClientViewSet)


