import csv

from django.core.management import BaseCommand
from django.db import IntegrityError

from recipes.models import Tag


class Command(BaseCommand):
    def handle(self, *args, **options):
        self.import_tags()
        print('Загрузка тегов завершена.')

    def import_tags(self, file='tags.csv'):
        print(f'Загрузка данных из {file}')
        path = f'./recipes/management/commands/data/{file}'
        try:
            with open(path, newline='', encoding='utf-8') as f:
                reader = csv.reader(f)
                tags_to_create = []
                for row in reader:
                    tags_to_create.append(
                        Tag(name=row[0], color=row[1], slug=row[2])
                    )
                Tag.objects.bulk_create(tags_to_create, ignore_conflicts=True)
        except FileNotFoundError:
            print(f"Файл {file} не найден.")
        except IntegrityError:
            print("Произошла ошибка при создании тегов.")
