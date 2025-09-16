from django.shortcuts import render
from .models import Promotion
from datetime import datetime

def promotions(request):
    active_promotions = Promotion.objects.filter(active=True, end_date__gte=datetime.now())
    return render(request, 'marketing/promotions.html', {'promotions': active_promotions})