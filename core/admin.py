from django.contrib import admin
from .models import MasterInfo
from .models import Document

@admin.register(MasterInfo)
class MasterInfoAdmin(admin.ModelAdmin):
    list_display = ['name', 'experience', 'specialization']
    list_editable = ['experience', 'specialization']


@admin.register(Document)
class DocumentAdmin(admin.ModelAdmin):
    list_display = ['title', 'slug', 'order', 'is_active', 'updated_at']
    list_editable = ['order', 'is_active']
    search_fields = ['title', 'content']
    prepopulated_fields = {'slug': ('title',)}