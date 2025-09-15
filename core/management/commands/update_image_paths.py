from django.core.management.base import BaseCommand
from core.models import Product

class Command(BaseCommand):
    help = 'Updates product image paths to include products/ prefix'

    def handle(self, *args, **options):
        products = Product.objects.all()
        count = 0
        for product in products:
            if product.image and not product.image.name.startswith('products/'):
                product.image.name = f'products/{product.image.name}'
                product.save()
                count += 1
        self.stdout.write(self.style.SUCCESS(f'Successfully updated {count} image paths.'))