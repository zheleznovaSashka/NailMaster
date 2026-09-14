from django.contrib import admin
from .models import Work

@admin.register(Work)
class WorkAdmin(admin.ModelAdmin):
    list_display = ['title', 'created_at', 'is_featured']
    list_filter = ['is_featured', 'created_at']
    search_fields = ['title', 'description']
    list_editable = ['is_featured']
