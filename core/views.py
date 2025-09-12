from django.shortcuts import render, redirect, get_object_or_404
from django.contrib.auth.decorators import login_required
from .models import Product, Category, Cart

def home(request):
    return render(request, 'home.html', {'title': 'Welcome to BharatBloom'})

def shop(request):
    products = Product.objects.filter(available=True)
    categories = Category.objects.all()
    query = request.GET.get('q')
    if query:
        products = products.filter(name__icontains=query)
    category_slug = request.GET.get('category')
    if category_slug:
        products = products.filter(category__slug=category_slug)
    return render(request, 'shop.html', {
        'title': 'Shop',
        'products': products,
        'categories': categories
    })

@login_required
def add_to_cart(request, product_id):
    product = get_object_or_404(Product, id=product_id)
    cart_item, created = Cart.objects.get_or_create(
        user=request.user,
        product=product,
        defaults={'quantity': 1}
    )
    if not created:
        cart_item.quantity += 1
        cart_item.save()
    return redirect('cart')

@login_required
def cart(request):
    cart_items = Cart.objects.filter(user=request.user)
    total_price = sum(item.product.price * item.quantity for item in cart_items)
    return render(request, 'cart.html', {
        'title': 'Your Cart',
        'cart_items': cart_items,
        'total_price': total_price
    })

@login_required
def remove_from_cart(request, product_id):
    cart_item = get_object_or_404(Cart, user=request.user, product_id=product_id)
    cart_item.delete()
    return redirect('cart')