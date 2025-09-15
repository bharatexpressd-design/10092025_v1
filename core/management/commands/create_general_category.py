from django.core.management.base import BaseCommand
from core.models import Category

class Command(BaseCommand):
    help = 'Create a default General category if it does not exist'

    def handle(self, *args, **kwargs):
        if not Category.objects.filter(name="General").exists():
            Category.objects.create(name="General", slug="general")
            self.stdout.write(self.style.SUCCESS('Successfully created General category'))
        else:
            self.stdout.write(self.style.WARNING('General category already exists'))