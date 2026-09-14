from django.urls import path
from . import views

app_name = 'users'

urlpatterns = [
    path('profile/', views.profile_view, name='profile'),
    path('logout/', views.logout_view, name='logout'),
    path('register/', views.register_view, name='register'),

    # Избранное
    path('favorites/', views.favorites_view, name='favorites'),
    path('favorites/clear/', views.clear_favorites, name='clear_favorites'),
    path('favorites/work/<int:work_id>/toggle/', views.toggle_work_favorite, name='toggle_work_favorite'),
    path('favorites/course/<int:course_id>/toggle/', views.toggle_course_favorite, name='toggle_course_favorite'),
]