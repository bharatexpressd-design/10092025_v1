from django.shortcuts import render
from .models import Product, Category

def home(request):
    return render(request, 'home.html', {'title': 'Welcome to BestEcom'})

def shop(request):
    # Get all available products
    products = Product.objects.filter(available=True)
    categories = Category.objects.all()

    # Search by product name
    query = request.GET.get('q')
    if query:
        products = products.filter(name__icontains=query)

    # Filter by category slug
    category_slug = request.GET.get('category')
    if category_slug:
        products = products.filter(category__slug=category_slug)

    return render(request, 'shop.html', {
        'title': 'Shop',
        'products': products,
        'categories': categories
    })