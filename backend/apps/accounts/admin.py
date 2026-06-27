from django.contrib import admin
from django.contrib.auth.admin import UserAdmin as BaseUserAdmin
from .models import User, Parent, Child


@admin.register(User)
class UserAdmin(BaseUserAdmin):
    list_display = ['email', 'username', 'role', 'is_active']
    list_filter = ['role', 'is_active']
    fieldsets = BaseUserAdmin.fieldsets + (
        ('役割・言語', {'fields': ('role', 'language')}),
    )


@admin.register(Parent)
class ParentAdmin(admin.ModelAdmin):
    list_display = ['name_ja', 'name_en', 'phone']


@admin.register(Child)
class ChildAdmin(admin.ModelAdmin):
    list_display = ['name_ja', 'class_name', 'parent', 'enrolled_at']
