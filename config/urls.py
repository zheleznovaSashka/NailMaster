from django.contrib import admin
from django.urls import path, include
from django.conf import settings
from django.conf.urls.static import static
from django.contrib.auth import views as auth_views
from users.views import register_view, logout_view

urlpatterns = [
    path('admin/', admin.site.urls),
    path('', include('core.urls')),
    path('portfolio/', include('portfolio.urls')),
    path('courses/', include('courses.urls')),
    path('reviews/', include('reviews.urls')),
    path('contacts/', include('contacts.urls')),
    path('users/', include('users.urls')),
    path('orders/', include('orders.urls')),
    path('cart/', include('cart.urls')),
    path('dashboard/', include('dashboard.urls')),

    # Аутентификация
    path('login/', auth_views.LoginView.as_view(template_name='users/login.html'), name='login'),
    path('logout/', logout_view, name='logout'),
    path('register/', register_view, name='register'),

    # 🔐 ВОССТАНОВЛЕНИЕ ПАРОЛЯ
    path('password-reset/',
         auth_views.PasswordResetView.as_view(
             template_name='users/password_reset.html',
             email_template_name='users/password_reset_email.html',
             subject_template_name='users/password_reset_subject.txt',
             success_url='/password-reset/done/'
         ),
         name='password_reset'),

    path('password-reset/done/',
         auth_views.PasswordResetDoneView.as_view(
             template_name='users/password_reset_done.html'
         ),
         name='password_reset_done'),

    path('password-reset-confirm/<uidb64>/<token>/',
         auth_views.PasswordResetConfirmView.as_view(
             template_name='users/password_reset_confirm.html',
             success_url='/password-reset-complete/'
         ),
         name='password_reset_confirm'),

    path('password-reset-complete/',
         auth_views.PasswordResetCompleteView.as_view(
             template_name='users/password_reset_complete.html'
         ),
         name='password_reset_complete'),
]

if settings.DEBUG:
    urlpatterns += static(settings.MEDIA_URL, document_root=settings.MEDIA_ROOT)
    urlpatterns += static(settings.STATIC_URL, document_root=settings.STATIC_ROOT)