from django.contrib import admin
from django.contrib.auth.admin import UserAdmin as DefaultUserAdmin
from .models import User

@admin.register(User)
class UserAdmin(DefaultUserAdmin):
    #  add role field into admins user form
    fieldsets = DefaultUserAdmin.fieldsets + ( (None, {'fields': ('role',),}), )

    add_fieldsets = DefaultUserAdmin.add_fieldsets + ( (None, {'fields': ('role',),}), )

    list_display = DefaultUserAdmin.list_display + ('role',)