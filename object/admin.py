from django.contrib import admin

from .models import *
class ObjectAdditionalEquipmentInline (admin.TabularInline):
    model = ObjectAdditionalEquipment
    extra = 0

class ObjectAdmin(admin.ModelAdmin):
    model = Object
    inlines = [ObjectAdditionalEquipmentInline]
admin.site.register(Object,ObjectAdmin)
admin.site.register(ObjectContact)
admin.site.register(ObjectFile)
admin.site.register(ObjectAdditionalEquipment)
admin.site.register(AdditionalEquipmentModel)
admin.site.register(AdditionalEquipmentCategory)

