from django.db import models
from core.models import Order

class Shipment(models.Model):
    order = models.ForeignKey(Order, on_delete=models.CASCADE)
    tracking_number = models.CharField(max_length=50, unique=True)
    status = models.CharField(max_length=20, choices=[
        ('PENDING', 'Pending'),
        ('SHIPPED', 'Shipped'),
        ('DELIVERED', 'Delivered')
    ], default='PENDING')
    updated_at = models.DateTimeField(auto_now=True)

    def __str__(self):
        return f"Shipment {self.tracking_number} for Order {self.order.razorpay_order_id}"