from django.contrib import admin
from django.contrib.auth.admin import Group, UserAdmin
from django.utils.translation import gettext_lazy as _
from users.models import User


class MyUserAdmin(UserAdmin):
    '''Класс для вывода на странице админа
    информации о пользователе.'''
    fieldsets = (
        (None, {'fields': ('email', 'password')}),
        (_('Personal info'), {'fields': ('first_name', 'last_name', 'avatar')}),
        (
            _('Permissions'),
            {
                'fields': (
                    'is_active',
                    'is_staff',
                    'is_superuser',
                    'groups',
                    'user_permissions',
                ),
            },
        ),
        (_('Important dates'), {'fields': ('last_login', 'date_joined')}),
    )
    add_fieldsets = (
        (
            None,
            {
                'classes': ('wide',),
                'fields': ('email', 'first_name', 'last_name', 
                           'password1', 'password2'),
            },
        ),
    )
    list_display = (
        'id',
        'email',
        'first_name',
        'last_name',
        'avatar',
        'gender',
        'is_staff'
    )
    list_filter = ('email',)
    ordering = ('email',)
    search_fields = ('first_name', 'last_name', 'email')


admin.site.register(User, MyUserAdmin)
admin.site.unregister(Group)
