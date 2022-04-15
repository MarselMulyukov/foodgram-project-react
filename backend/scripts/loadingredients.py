from recipes.models import Ingredient
import csv


def run():
    with open('recipes/ingredients.csv', encoding='UTF8') as file:
        reader = csv.reader(file)
        Ingredient.objects.all().delete()

        for row in reader:
            print(row)

            ingredient = Ingredient(name=row[0], measurement_unit=row[1])
            ingredient.save()
