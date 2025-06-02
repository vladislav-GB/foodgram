from django.core.management.base import BaseCommand
from recipes.models import Ingredient
import csv
import os

class Command(BaseCommand):
    help = 'Загрузка ингредиентов из CSV файла'

    def handle(self, *args, **options):
        file_path = os.path.join('data', 'ingredients.csv')
        
        with open(file_path, 'r', encoding='utf-8') as f:
            reader = csv.reader(f)
            for row in reader:
                Ingredient.objects.get_or_create(
                    name=row[0],
                    measurement_unit=row[1]
                )
        
        self.stdout.write(self.style.SUCCESS('Ингредиенты успешно загружены!'))