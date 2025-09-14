from django.shortcuts import render, redirect, get_object_or_404
from django.contrib.auth.decorators import login_required
from django.conf import settings
from django.http import HttpResponseBadRequest, JsonResponse, FileResponse
from django.views.decorators.csrf import csrf_exempt
from django.contrib import messages
from django.contrib.auth.forms import UserChangeForm
from django.contrib.auth.models import User
from django import forms
from .models import Product, Cart, Category, Order, OrderItem
import razorpay
import hmac
import hashlib
import json

class CustomUserChangeForm(UserChangeForm):
    class Meta:
        model = User
        fields = ('first_name', 'last_name', 'email')

def home(request):
    return render(request, 'home.html')

def shop(request):
    products = Product.objects.all()
    categories = Category.objects.all()
    query = request.GET.get('q')
    category = request.GET.get('category')
    material = request.GET.get('material')
    region = request.GET.get('region')
    if query:
        products = products.filter(name__icontains=query)
    if category:
        products = products.filter(category__slug=category)
    if material:
        products = products.filter(material__icontains=material)
    if region:
        products = products.filter(region__icontains=region)
    return render(request, 'shop.html', {'products': products, 'categories': categories})

@login_required
def cart(request):
    cart_items = Cart.objects.filter(user=request.user)
    total_price = sum(item.product.price * item.quantity for item in cart_items)
    return render(request, 'cart.html', {'cart_items': cart_items, 'total_price': total_price})

@login_required
def add_to_cart(request, product_id):
    try:
        product = Product.objects.get(id=product_id)
        cart_item, created = Cart.objects.get_or_create(user=request.user, product=product)
        quantity = 1
        if request.method == 'POST':
            quantity = int(request.POST.get('quantity', 1))
            if quantity < 1:
                return render(request, 'error.html', {'message': 'Invalid quantity'}, status=400)
        new_quantity = cart_item.quantity + quantity if not created else quantity
        if new_quantity > product.stock:
            return render(request, 'error.html', {'message': f'Cannot add more {product.name}. Only {product.stock} in stock.'}, status=400)
        cart_item.quantity = new_quantity
        cart_item.save()
    except Product.DoesNotExist:
        return render(request, 'error.html', {'message': 'Product not found'}, status=404)
    return redirect('cart')

@login_required
def remove_from_cart(request, product_id):
    try:
        cart_item = Cart.objects.get(user=request.user, product_id=product_id)
        if request.method == 'POST' and request.POST.get('remove_all') == 'true':
            cart_item.delete()
        elif cart_item.quantity > 1:
            cart_item.quantity -= 1
            cart_item.save()
        else:
            cart_item.delete()
    except Cart.DoesNotExist:
        return render(request, 'error.html', {'message': 'Cart item not found'}, status=404)
    return redirect('cart')

@login_required
def checkout(request):
    cart_items = Cart.objects.filter(user=request.user)
    total_price = sum(item.product.price * item.quantity for item in cart_items)
    if not cart_items or total_price < 1:
        return HttpResponseBadRequest('Cart is empty or total price is too low')
    client = razorpay.Client(auth=(settings.RAZORPAY_KEY_ID, settings.RAZORPAY_KEY_SECRET))
    payment_data = {
        'amount': int(total_price * 100),
        'currency': 'INR',
        'receipt': f'order_{request.user.id}',
        'payment_capture': 1,
        'notes': {'mode': 'test', 'test_payment': 'true'}
    }
    try:
        order = client.order.create(data=payment_data)
        Order.objects.create(
            user=request.user,
            razorpay_order_id=order['id'],
            total_amount=total_price,
            status='Pending'
        )
    except razorpay.errors.BadRequestError as e:
        print("Razorpay Error:", str(e))
        return HttpResponseBadRequest(f'Payment error: {str(e)}')
    return render(request, 'checkout.html', {
        'cart_items': cart_items,
        'total_price': total_price,
        'razorpay_order_id': order['id'],
        'razorpay_key_id': settings.RAZORPAY_KEY_ID,
        'user': request.user
    })

@csrf_exempt
@login_required
def payment_success(request):
    if request.method != 'POST':
        return HttpResponseBadRequest('Invalid request method')
    try:
        data = json.loads(request.body)
        payment_id = data.get('payment_id')
        order_id = data.get('order_id')
        signature = data.get('signature')
        client = razorpay.Client(auth=(settings.RAZORPAY_KEY_ID, settings.RAZORPAY_KEY_SECRET))
        params_dict = {
            'razorpay_order_id': order_id,
            'razorpay_payment_id': payment_id,
            'razorpay_signature': signature
        }
        client.utility.verify_payment_signature(params_dict)
        order = Order.objects.get(razorpay_order_id=order_id, user=request.user)
        order.razorpay_payment_id = payment_id
        order.razorpay_signature = signature
        order.status = 'Completed'
        order.save()
        cart_items = Cart.objects.filter(user=request.user)
        for item in cart_items:
            OrderItem.objects.create(
                order=order,
                product=item.product,
                quantity=item.quantity,
                price=item.product.price
            )
        Cart.objects.filter(user=request.user).delete()
        return JsonResponse({'status': 'success', 'message': 'Payment verified and cart cleared'})
    except (razorpay.errors.SignatureVerificationError, Order.DoesNotExist) as e:
        return JsonResponse({'status': 'error', 'message': str(e)}, status=400)

@login_required
def profile(request):
    if request.method == 'POST':
        form = CustomUserChangeForm(request.POST, instance=request.user)
        if form.is_valid():
            form.save()
            messages.success(request, 'Profile updated successfully!')
            return redirect('profile')
    else:
        form = CustomUserChangeForm(instance=request.user)
    return render(request, 'profile.html', {'form': form})

@login_required
def order_history(request):
    orders = Order.objects.filter(user=request.user).order_by('-created_at')
    return render(request, 'order_history.html', {'orders': orders})

def serve_media(request, path):
    return FileResponse(open(settings.MEDIA_ROOT / path, 'rb'))