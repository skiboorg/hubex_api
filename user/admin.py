from django.contrib import admin
from django.contrib.auth.admin import UserAdmin as BaseUserAdmin

from .models import *


class UserAdmin(BaseUserAdmin):
    list_display = (
        'login',
        'fio',
        'phone',
        'date_joined',

    )
    ordering = ('id',)

    add_fieldsets = (
        (None, {
            'classes': ('wide',),
            'fields': (
                "login",
                "fio",
                "phone",
                       'password1',
                       'password2',
                       ), }),)
    search_fields = ('id','login', 'fio', 'phone',)

    fieldsets = (
        (None, {'fields': ('login', 'password')}),
        ('Personal info',
         {'fields': (
             'role',
             'email',
                "fio",
                "phone",
                "is_driving",
                "avatar",
                "plain_password",

         )}
         ),
        ('Permissions', {'fields': ('is_staff', 'is_superuser', 'groups',)}),)

admin.site.register(User,UserAdmin)
admin.site.register(Role)




