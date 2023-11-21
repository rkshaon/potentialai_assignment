from django.contrib import admin
from django.contrib.auth.admin import UserAdmin as BaseUserAdmin

from user_api.models import User



class CustomUserAdmin(BaseUserAdmin):
    list_display = ('username', 'email', 'is_staff', 'is_superuser', 'is_vendor')
    list_filter = ('is_staff', 'is_superuser', 'is_vendor', 'groups')
    search_fields = ('username', 'email')
    ordering = ('username',)
    filter_horizontal = ('groups', 'user_permissions',)



admin.site.register(User)
