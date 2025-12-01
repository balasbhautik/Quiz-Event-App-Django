from django.contrib import admin
from django.contrib.auth.admin import UserAdmin as BaseUserAdmin
from django.utils.translation import gettext_lazy as _
from user_accounts.models import User

# Register your models here.

@admin.register(User)
class UserAdmin(BaseUserAdmin):
    model = User
    list_display = ['first_name','last_name','email']
    list_filter = ('is_staff','is_active','is_superuser')
    fieldsets = (
        (None, {'fields' : ('email','password')}),
        (_('personal_info'), {'fields':('first_name','last_name','profile_pic')}),
        (_('Permissions'), {'fields':('is_active','is_staff','is_superuser')}),
        (_('Important dates'), {'fields': ('date_joined',)}),
    )

    add_fieldsets = (
        (None, {
            'classes': ('wide',),
            'fields': ('email', 'password1', 'password2', 'is_staff', 'is_active')}
        ),
    )

    search_fields = ('email', 'first_name', 'last_name')



