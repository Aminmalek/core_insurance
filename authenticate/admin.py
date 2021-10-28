from django.contrib import admin
from . models import User
from django.contrib.auth.admin import UserAdmin


class CustomUserAdmin(UserAdmin):
    model = User
    filter_horizontal = ('user_permissions', 'groups', )
    list_display = ('username', 'first_name','last_name' ,'id',
                     'is_staff', 'last_login')
    fieldsets = (
        (None, {'fields': ('username', 'password')}),
        (('Personal info'), {
         'fields': ('first_name', 'last_name', 'email', 'cash', 'type', 'phone', 'bank_account_number')}),
        (('Permissions'), {
            'fields': ('is_active', 'is_staff', 'is_superuser', 'groups', 'user_permissions'),
        }),
        (('Important dates'), {'fields': ('last_login', 'date_joined')}),
    )


admin.site.register(User, CustomUserAdmin)
