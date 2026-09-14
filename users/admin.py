from django.contrib import admin
from django.contrib.auth.admin import UserAdmin
from .models import CustomUser

@admin.register(CustomUser)
class CustomUserAdmin(UserAdmin):
    list_display = ['email', 'username', 'phone', 'is_active', 'is_banned']
    list_filter = ['is_active', 'is_banned']
    search_fields = ['email', 'username', 'phone']
    list_editable = ['is_banned']
    
    fieldsets = (
        (None, {'fields': ('email', 'password')}),
        ('Личная информация', {'fields': ('username', 'phone', 'avatar')}),
        ('Права доступа', {'fields': ('is_active', 'is_staff', 'is_superuser', 'is_banned')}),
    )
    
    add_fieldsets = (
        (None, {
            'classes': ('wide',),
            'fields': ('email', 'username', 'password1', 'password2'),
        }),
    )
