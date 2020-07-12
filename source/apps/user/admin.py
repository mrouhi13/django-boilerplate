from django.contrib import admin
from django.contrib.auth.admin import UserAdmin
from django.utils.translation import ugettext_lazy as _

from apps.user.models import User


@admin.register(User)
class UserAdmin(UserAdmin):
    date_hierarchy = 'date_joined'
    fieldsets = [
        [None, {'fields': ['email', 'password']}],
        [_('Personal info'), {
            'fields': ['first_name', 'last_name']
        }],
        [_('Permissions'), {
            'classes': ['collapse'],
            'fields': ['is_active', 'is_staff', 'is_superuser', 'groups',
                       'user_permissions']
        }],
        [_('Important dates'), {
            'fields': ['last_login', 'date_joined']
        }],
    ]
    add_fieldsets = [
        [None, {
            'classes': ['wide'],
            'fields': ['email', 'password1', 'password2'],
        }],
    ]
    list_display = ['email', 'first_name', 'last_name', 'is_staff',
                    'is_superuser', 'is_active']
    search_fields = ['first_name', 'last_name', 'email']
    ordering = []
    readonly_fields = ['last_login', 'date_joined']
    autocomplete_fields = ['groups']