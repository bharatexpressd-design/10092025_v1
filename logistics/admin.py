from django.contrib import admin
from .models import Shipment

@admin.register(Shipment)
class ShipmentAdmin(admin.ModelAdmin):
    list_display = ['tracking_number', 'order', 'status', 'updated_at']
    list_filter = ['status']
    search_fields = ['tracking_number', 'order__razorpay_order_id']