import csv

from django.core.management import BaseCommand
from django.db import IntegrityError

from recipes.models import Ingredient


class Command(BaseCommand):
    def handle(self, *args, **options):
        self.import_ingredients()
        print('Загрузка ингредиентов завершена.')

    def import_ingredients(self, file='ingredients.csv'):
        print(f'Загрузка данных из {file}')
        path = f'./recipes/management/commands/data/{file}'
        try:
            with open(path, newline='', encoding='utf-8') as f:
                reader = csv.reader(f)
                ingredients_to_create = [
                    Ingredient(name=row[0], measurement_unit=row[1])
                    for row in reader
                ]
                Ingredient.objects.bulk_create(
                    ingredients_to_create, ignore_conflicts=True
                )
        except FileNotFoundError:
            print(f"Файл {file} не найден.")
        except IntegrityError:
            print(f"Произошла ошибка при создании ингредиентов.")
