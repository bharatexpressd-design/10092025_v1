from django.core.management.base import BaseCommand
from django.contrib.auth.models import User
from core.models import Product, Order, Category
from logistics.models import Shipment
from marketing.models import Promotion
from datetime import datetime, timedelta
from django.utils import timezone
from django.utils.text import slugify

class Command(BaseCommand):
    help = 'Populates sample data for testing logistics and marketing modules'

    def handle(self, *args, **kwargs):
        # Get or create user
        user, _ = User.objects.get_or_create(
            username='Test_1',
            defaults={'email': 'test1@example.com', 'password': 'testpassword123'}
        )
        if not user.has_usable_password():
            user.set_password('testpassword123')
            user.save()
        self.stdout.write(self.style.SUCCESS(f'User: {user.username}'))

        # Create sample category
        category, _ = Category.objects.get_or_create(
            name='Clothing',
            defaults={'slug': slugify('Clothing'), 'description': 'Traditional Indian clothing'}
        )
        self.stdout.write(self.style.SUCCESS(f'Category: {category.name}'))

        # Create sample products
        product1, _ = Product.objects.get_or_create(
            name='Handloom Saree',
            defaults={
                'price': 1500.00,
                'stock': 10,
                'image': '',
                'category': category,
                'material': 'Silk',
                'region': 'South India'
            }
        )
        product2, _ = Product.objects.get_or_create(
            name='Cotton Kurta',
            defaults={
                'price': 800.00,
                'stock': 20,
                'image': '',
                'category': category,
                'material': 'Cotton',
                'region': 'North India'
            }
        )
        self.stdout.write(self.style.SUCCESS(f'Products: {product1.name}, {product2.name}'))

        # Create sample orders
        order1, _ = Order.objects.get_or_create(
            user=user,
            razorpay_order_id='order_001',
            defaults={
                'total_amount': 1500.00,
                'status': 'Pending',
                'created_at': timezone.now(),
                'razorpay_payment_id': '',
                'razorpay_signature': ''
            }
        )
        order2, _ = Order.objects.get_or_create(
            user=user,
            razorpay_order_id='order_002',
            defaults={
                'total_amount': 800.00,
                'status': 'Pending',
                'created_at': timezone.now(),
                'razorpay_payment_id': '',
                'razorpay_signature': ''
            }
        )
        self.stdout.write(self.style.SUCCESS(f'Orders: {order1.razorpay_order_id}, {order2.razorpay_order_id}'))

        # Create sample shipments
        Shipment.objects.get_or_create(
            order=order1,
            tracking_number='TRACK001',
            defaults={'status': 'SHIPPED', 'updated_at': timezone.now()}
        )
        Shipment.objects.get_or_create(
            order=order2,
            tracking_number='TRACK002',
            defaults={'status': 'PENDING', 'updated_at': timezone.now()}
        )
        self.stdout.write(self.style.SUCCESS('Shipments: TRACK001, TRACK002'))

        # Create sample promotions
        Promotion.objects.get_or_create(
            product=product1,
            discount_percentage=10.00,
            start_date=timezone.now() - timedelta(days=1),
            defaults={'end_date': timezone.now() + timedelta(days=7), 'active': True}
        )
        Promotion.objects.get_or_create(
            product=product2,
            discount_percentage=15.00,
            start_date=timezone.now() - timedelta(days=1),
            defaults={'end_date': timezone.now() + timedelta(days=5), 'active': True}
        )
        self.stdout.write(self.style.SUCCESS('Promotions: 10% off Handloom Saree, 15% off Cotton Kurta'))