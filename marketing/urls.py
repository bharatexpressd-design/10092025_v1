from django.urls import path
from . import views

urlpatterns = [
    path('promotions/', views.promotions, name='promotions'),
]