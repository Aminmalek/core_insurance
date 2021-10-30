from django.contrib import admin
from . models import User
from django.contrib.auth.admin import UserAdmin


class CustomUserAdmin(UserAdmin):
    model = User
    filter_horizontal = []
    list_display = ('username', 'first_name', 'last_name', 'type','id','last_login')
    fieldsets = (
        (None, {'fields': ('username', 'password')}),
        (('Personal info'), {
         'fields': ('first_name', 'last_name', 'cash', 'type', 'phone', 'bank_account_number')}),
        (('Permissions'), {
            'fields': ('is_active', 'is_superuser',),
        }),
        (('Important dates'), {'fields': ('last_login',)}),
    )
    list_filter = ('is_superuser', 'is_active',)
    
admin.site.register(User, CustomUserAdmin)
