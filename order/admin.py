from django.contrib import admin

from .models import *
class CheckListInputInline (admin.TabularInline):
    model = CheckListInput
    extra = 0
class CheckListTableInline (admin.TabularInline):
    model = CheckListTable
    extra = 0

class CheckListTableInputInline (admin.TabularInline):
    model = CheckListTableInput
    extra = 0


class StageGroupSelectInline (admin.TabularInline):
    model = StageGroupSelect
    extra = 0
class CheckListTableHistoryInline (admin.TabularInline):
    model = CheckListTableHistory
    extra = 0

class CheckListDataHistoryInline (admin.TabularInline):
    model = CheckListDataHistory
    extra = 0

class StageButtontInline (admin.TabularInline):
    model = StageButton
    fk_name = 'stage'
    extra = 0

class CheckListAdmin(admin.ModelAdmin):
    model = CheckList
    inlines = [CheckListInputInline,CheckListTableInline]

class CheckListTableAdmin(admin.ModelAdmin):
    model = CheckList
    inlines = [CheckListTableInputInline]

class CheckListHistoryAdmin(admin.ModelAdmin):
    model = CheckListHistory
    inlines = [CheckListDataHistoryInline, CheckListTableHistoryInline]



class StageAdmin(admin.ModelAdmin):
    model = Stage
    inlines = [StageGroupSelectInline,StageButtontInline]


admin.site.register(Status)
admin.site.register(InputField)
admin.site.register(CheckList,CheckListAdmin)
#admin.site.register(CheckListInput)
admin.site.register(Stage,StageAdmin)
admin.site.register(CheckListData)
admin.site.register(Order)
admin.site.register(Type)
admin.site.register(WorkType)
admin.site.register(StageLog)
admin.site.register(CheckListTable,CheckListTableAdmin)
admin.site.register(CheckListTableInput)
admin.site.register(CheckListTableInputField)
admin.site.register(CheckListTableData)
admin.site.register(CheckListHistory, CheckListHistoryAdmin)


