from django.contrib import admin
from .models import Course

@admin.register(Course)
class CourseAdmin(admin.ModelAdmin):
    list_display = ['title', 'price', 'duration', 'created_at']
    search_fields = ['title', 'description']
    list_filter = ['duration']
