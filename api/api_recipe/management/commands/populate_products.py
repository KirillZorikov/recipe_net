import csv

from django.core.management import BaseCommand

from api.api_recipe.models import Product, Unit

CSV_PRODUCTS = r'dummy_data/ingredients.csv'


class Command(BaseCommand):
    def handle(self, *args, **kwargs):
        with open(CSV_PRODUCTS, 'rt') as file:
            reader = csv.reader(file, dialect='excel')
            data_rows = [row for row in reader]
            for data in data_rows:
                product_title, unit_title = data
                unit = Unit.objects.get_or_create(title=unit_title)[0]
                Product.objects.get_or_create(title=product_title, unit=unit)
        print('Success!')
