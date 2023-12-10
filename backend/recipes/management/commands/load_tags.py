import csv
from django.core.management import BaseCommand
from django.db import IntegrityError

from recipes.models import Tag


class Command(BaseCommand):

    def handle(self, *args, **options):
        try:
            self.import_tags()
            print('Загрузка тегов завершена.')
        except FileNotFoundError as e:
            print(f'Ошибка при открытии файла: {e}')

    def import_tags(self, file='tags.csv'):
        print(f'Загрузка данных из {file}')
        path = f'./recipes/management/commands/data/{file}'
        try:
            with open(path, newline='', encoding='utf-8') as f:
                reader = csv.reader(f)
                tags_to_create = []
                for row in reader:
                    try:
                        name, color, slug = row  # Распаковка
                        tags_to_create.append(Tag(name=name,
                                                  color=color,
                                                  slug=slug))
                    except IntegrityError:
                        print(f"Тег {name} уже существует.")
                Tag.objects.bulk_create(tags_to_create, ignore_conflicts=True)
        except FileNotFoundError:
            raise FileNotFoundError(f'Файл {file} не найден.')
