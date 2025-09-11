from django.shortcuts import render
from .models import Product

def home(request):
    return render(request, 'home.html', {'title': 'Welcome to BestEcom'})

def shop(request):
    products = Product.objects.filter(available=True)
    return render(request, 'shop.html', {'title': 'Shop', 'products': products})