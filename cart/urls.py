from django.urls import path
from . import views

app_name = 'cart'

urlpatterns = [
    path('', views.cart_view, name='view'),
    path('add/<int:course_id>/', views.add_to_cart, name='add'),
    path('remove/<int:course_id>/', views.remove_from_cart, name='remove'),
    path('clear/', views.clear_cart, name='clear'),
    path('checkout/', views.checkout, name='checkout'),
]