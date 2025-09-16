from django.shortcuts import render
from django.contrib.auth.decorators import login_required
from .models import Shipment

@login_required
def track_order(request):
    shipments = Shipment.objects.filter(order__user=request.user)
    return render(request, 'logistics/track_order.html', {'shipments': shipments})