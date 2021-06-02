from django.contrib import admin
from .models import *
from django.contrib.auth.admin import UserAdmin
from .forms import *


admin.site.register(Role)
admin.site.register(Permission)

class CustomUserAdmin(UserAdmin):
    add_form = CustomUserCreationForm
    form = CustomUserChangeForm
    model = User
    list_display = ('email', 'is_staff', 'is_active',)
    list_filter = ('email', 'is_staff', 'is_active',)
    fieldsets = (
        (None, {'fields': ('email', 'password','first_name','last_name')}),
        ('Permissions', {'fields': ('role','is_staff','is_superuser', 'is_active','groups')}),
    )
    add_fieldsets = (
        (None, {
            'classes': ('wide',),
         
            'fields': ('email', 'first_name','last_name','password1', 'password2', 'is_staff', 'is_active')}
        ),
    )
    search_fields = ('email',)
    ordering = ('email',)



admin.site.register(User, CustomUserAdmin)
