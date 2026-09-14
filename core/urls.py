from django.urls import path
from . import views


urlpatterns = [
    path('', views.home_view, name='home'),
    path('pages/<slug:slug>/', views.document_view, name='document'),
]