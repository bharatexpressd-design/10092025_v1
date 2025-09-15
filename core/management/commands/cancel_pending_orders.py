from django.core.management.base import BaseCommand
from django.utils import timezone
from datetime import timedelta
from core.models import Order

class Command(BaseCommand):
    help = 'Cancels pending orders older than 24 hours'

    def handle(self, *args, **options):
        threshold = timezone.now() - timedelta(hours=24)
        pending_orders = Order.objects.filter(status='Pending', created_at__lt=threshold)
        count = pending_orders.count()
        pending_orders.update(status='Cancelled')
        self.stdout.write(self.style.SUCCESS(f'Successfully cancelled {count} pending orders.'))