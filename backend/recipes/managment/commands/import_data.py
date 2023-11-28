import csv

from django.core.management.base import BaseCommand

from recipes.models import Ingredient


PATH = 'data/'


class Command(BaseCommand):

    def get_arguments(self, parser):
        parser.add_argument(
            '--delete-existing',
            action='store_true',
            dest='delete_existing',
            default=False,
        )

    def handle(self, *args, **options):
        with open(PATH + 'ingredients.csv', 'r', newline='') as csvfile:
            reader = csv.DictReader(csvfile)
            records = []
            for row in reader:
                records.append(Ingredient(
                    name=row['name'],
                    measurement_unit=row['measurement_unit']))
            Ingredient.objects.bulk_create(records)
            self.stdout.write(self.style.SUCCESS('Данные импортированы'))
            csvfile.close()
