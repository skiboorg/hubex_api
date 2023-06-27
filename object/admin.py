from django.contrib import admin

from .models import *

admin.site.register(Object)
admin.site.register(ObjectContact)
admin.site.register(ObjectFile)
admin.site.register(ObjectAdditionalEquipment)
admin.site.register(AdditionalEquipmentModel)
admin.site.register(AdditionalEquipmentCategory)

