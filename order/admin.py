from django.contrib import admin

from .models import *
class CheckListInputInline (admin.TabularInline):
    model = CheckListInput
    extra = 0

class CheckListAdmin(admin.ModelAdmin):
    model = CheckList
    inlines = [CheckListInputInline]
admin.site.register(Status)
admin.site.register(InputField)
admin.site.register(CheckList,CheckListAdmin)
admin.site.register(CheckListInput)
admin.site.register(Stage)
admin.site.register(CheckListData)
admin.site.register(Order)
admin.site.register(StageLog)


