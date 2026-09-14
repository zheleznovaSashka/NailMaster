from django.contrib import admin
from .models import MasterInfo

@admin.register(MasterInfo)
class MasterInfoAdmin(admin.ModelAdmin):
    list_display = ['name', 'experience', 'specialization']
    list_editable = ['experience', 'specialization']
