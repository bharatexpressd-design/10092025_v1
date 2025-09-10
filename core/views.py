from django.shortcuts import render

def home(request):
    return render(request, 'home.html', {'title': 'Welcome to BestEcom'})

def shop(request):
    return render(request, 'shop.html', {'products': []})