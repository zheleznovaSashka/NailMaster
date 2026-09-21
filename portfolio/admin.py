from django.contrib import admin
from .models import Work, WorkView


@admin.register(Work)
class WorkAdmin(admin.ModelAdmin):
    list_display = ['title', 'views', 'is_featured', 'created_at']
    list_editable = ['is_featured']
    list_filter = ['is_featured', 'created_at']
    search_fields = ['title', 'description']
    readonly_fields = ['views']


@admin.register(WorkView)
class WorkViewAdmin(admin.ModelAdmin):
    list_display = ['work', 'user', 'session_key', 'created_at']
    list_filter = ['created_at']
    search_fields = ['work__title', 'user__username']
    date_hierarchy = 'created_at'
    readonly_fields = ['work', 'user', 'session_key', 'created_at']
