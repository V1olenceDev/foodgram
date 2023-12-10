import csv
from django.core.management import BaseCommand
from django.db import IntegrityError

from recipes.models import Ingredient


class Command(BaseCommand):

    def handle(self, *args, **options):
        try:
            self.import_ingredients()
            print('Загрузка ингредиентов завершена.')
        except FileNotFoundError as e:
            print(f'Ошибка при открытии файла: {e}')

    def import_ingredients(self, file='ingredients.csv'):
        print(f'Загрузка данных из {file}')
        path = f'./recipes/management/commands/data/{file}'
        try:
            with open(path, newline='', encoding='utf-8') as f:
                reader = csv.reader(f)
                ingredients_to_create = []
                for row in reader:
                    try:
                        name, measurement_unit = row
                        ingredients_to_create.append(Ingredient(
                            name=name,
                            measurement_unit=measurement_unit))
                    except IntegrityError:
                        print(f"Ингредиент {name} уже существует.")
                Ingredient.objects.bulk_create(ingredients_to_create,
                                               ignore_conflicts=True)
        except FileNotFoundError:
            raise FileNotFoundError(f'Файл {file} не найден.')
