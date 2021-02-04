from django.db import models


class Ingredient(models.Model):
    display_name = models.CharField(max_length=100)

    def __str__(self):
        return f"{self.display_name}"

class Unit(models.Model):
    long_name = models.CharField(max_length=100)
    abbreviation = models.CharField(max_length=10)

    def __str__(self):
        return f"{self.long_name} ({self.abbreviation})"

class Recipe(models.Model):
    display_name = models.CharField(max_length=100)
    servings = models.IntegerField(default=1)

    # Macros per portion
    calories_pp = models.IntegerField(default=0)
    grams_protein_pp = models.FloatField(default=0)
    grams_carbs_pp = models.FloatField(default=0)
    grams_fat_pp = models.FloatField(default=0)

    def __str__(self):
        return (f"{self.display_name} "
                f"({self.calories_pp}kcal,"
                f"{self.grams_protein_pp}P,"
                f"{self.grams_carbs_pp}C,"
                f"{self.grams_fat_pp}F)")

class RecipeIngredient(models.Model):
    ingredient = models.ForeignKey(Ingredient, on_delete=models.PROTECT)
    recipe = models.ForeignKey(Recipe, on_delete=models.CASCADE)
    quantity = models.FloatField()
    unit = models.ForeignKey(Unit, on_delete=models.PROTECT)

    def __str__(self):
        return f"{self.quantity}{self.unit.abbreviation} {self.ingredient}"

class Meal(models.Model):
    MEALS = [('B', 'Breakfast'),
             ('L', 'Lunch'),
             ('D', 'Dinner')]
    date = models.DateField()
    meal = models.CharField(max_length=9, choices=MEALS, default='D')
    recipe = models.ForeignKey(Recipe, on_delete=models.CASCADE)

    class Meta:
        unique_together = ('date', 'meal')
