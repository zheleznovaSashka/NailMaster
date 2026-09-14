from django.contrib import admin
from .models import Review, ScreenshotReview


@admin.register(Review)
class ReviewAdmin(admin.ModelAdmin):
    list_display = ['user', 'review_type', 'rating', 'is_approved', 'created_at']
    list_filter = ['is_approved', 'review_type', 'rating']
    search_fields = ['user__username', 'text']
    list_editable = ['is_approved']


@admin.register(ScreenshotReview)
class ScreenshotReviewAdmin(admin.ModelAdmin):
    list_display = ['title', 'source', 'is_featured', 'order', 'created_at']
    list_filter = ['source', 'is_featured']
    list_editable = ['is_featured', 'order']
    search_fields = ['title']