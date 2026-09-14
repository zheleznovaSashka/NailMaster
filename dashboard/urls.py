from django.urls import path
from . import views

app_name = 'dashboard'

urlpatterns = [
    path('', views.dashboard_home, name='home'),

    # Работы
    path('works/', views.works_list, name='works_list'),
    path('works/create/', views.work_create, name='work_create'),
    path('works/<int:pk>/edit/', views.work_edit, name='work_edit'),
    path('works/<int:pk>/delete/', views.work_delete, name='work_delete'),
    path('works/<int:pk>/toggle/', views.work_toggle_featured, name='work_toggle'),

    # Курсы
    path('courses/', views.courses_list, name='courses_list'),
    path('courses/create/', views.course_create, name='course_create'),
    path('courses/<int:pk>/edit/', views.course_edit, name='course_edit'),
    path('courses/<int:pk>/delete/', views.course_delete, name='course_delete'),

    # Скрины отзывов
    path('screenshots/', views.screenshots_list, name='screenshots_list'),
    path('screenshots/create/', views.screenshot_create, name='screenshot_create'),
    path('screenshots/<int:pk>/edit/', views.screenshot_edit, name='screenshot_edit'),
    path('screenshots/<int:pk>/delete/', views.screenshot_delete, name='screenshot_delete'),
    path('screenshots/<int:pk>/toggle/', views.screenshot_toggle_featured, name='screenshot_toggle'),

    # Отзывы
    path('reviews/', views.reviews_list, name='reviews_list'),
    path('reviews/<int:pk>/approve/', views.review_approve, name='review_approve'),
    path('reviews/<int:pk>/reject/', views.review_reject, name='review_reject'),
    path('reviews/<int:pk>/delete/', views.review_delete, name='review_delete'),

    # Информация о мастере
    path('master/', views.master_edit, name='master_edit'),

    # Контакты
    path('contacts/', views.contacts_edit, name='contacts_edit'),

    # Пользователи
    path('users/', views.users_list, name='users_list'),
    path('users/<int:pk>/', views.user_detail, name='user_detail'),
    path('users/<int:pk>/toggle-ban/', views.user_toggle_ban, name='user_toggle_ban'),
    path('users/<int:pk>/toggle-staff/', views.user_toggle_staff, name='user_toggle_staff'),

    # Заказы
    path('orders/', views.orders_list, name='orders_list'),
    path('orders/<int:pk>/', views.order_detail_dashboard, name='order_detail'),
    path('orders/<int:pk>/status/<str:status>/', views.order_change_status, name='order_change_status'),
    path('orders/<int:pk>/delete/', views.order_delete, name='order_delete'),

]
