from django.urls import path
from . import views

urlpatterns = [
    path('', views.home, name='home'),
    path('shop/', views.shop, name='shop'),
    path('cart/', views.cart, name='cart'),
    path('cart/add/<int:product_id>/', views.add_to_cart, name='cart_add'),
    path('cart/remove/<int:product_id>/', views.remove_from_cart, name='cart_remove'),
]