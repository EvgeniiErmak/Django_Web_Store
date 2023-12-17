from django.core.management.base import BaseCommand
from django.db import transaction
from catalog.models import Category


class Command(BaseCommand):
    help = 'Populate database with sample data'

    def handle(self, *args, **options):
        with transaction.atomic():
            self.stdout.write(self.style.SUCCESS('Clearing existing data...'))
            Category.objects.all().delete()

            self.stdout.write(self.style.SUCCESS('Populating data...'))
            Category.objects.create(name='Electronics', description='Electronic devices')
            Category.objects.create(name='Clothing', description='Fashion and apparel')
            Category.objects.create(name='Books', description='Books and literature')

            self.stdout.write(self.style.SUCCESS('Data population complete.'))
