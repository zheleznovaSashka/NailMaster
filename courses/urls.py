from django.urls import path
from . import views

app_name = 'courses'  # ← ДОЛЖНО БЫТЬ!

urlpatterns = [
    path('', views.course_list, name='list'),
    path('<int:pk>/', views.course_detail, name='detail'),
]
