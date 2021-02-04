import datetime 

from django.contrib.auth.decorators import login_required
from django.http import HttpResponse, HttpResponseRedirect
from django.shortcuts import get_object_or_404, render
from django.urls import reverse

from .models import Recipe, Ingredient, RecipeIngredient, Unit, Meal

def index(request):
    return HttpResponseRedirect(reverse("kansas:week"))

def week(request):
    def get_meal_or_none(*, meal=None, date=None):
        try:
            return Meal.objects.get(meal=meal, date=date)
        except Meal.DoesNotExist:
            return None

    today = datetime.date.today()
    start_of_week = today - datetime.timedelta(days=today.weekday())
    days=[]
    for dow in range(7):
        date = (start_of_week + datetime.timedelta(days=dow)).strftime("%Y-%m-%d")
        day = {
            "date": date,
            "today": date == today.strftime("%Y-%m-%d"),
            "meals": {
                m: get_meal_or_none(meal=m, date=date)
                for m in ["B", "L", "D"]
            },
        }
        day["calories"] = sum([
            m.recipe.calories_pp
            for m in day["meals"].values()
            if m is not None
        ])
        day["protein"] = sum([
            m.recipe.grams_protein_pp
            for m in day["meals"].values()
            if m is not None
        ])
        day["carbs"] = sum([
            m.recipe.grams_carbs_pp
            for m in day["meals"].values()
            if m is not None
        ])
        day["fat"] = sum([
            m.recipe.grams_fat_pp
            for m in day["meals"].values()
            if m is not None
        ])
        days.append(day)
    return render(request, 'kansas/week.html', {
        'days': days,
    })

def _save_recipe_from_request(recipe, request):
    # @@@ - TODO: Make this slightly more robust about form items missing
    ingredients = []
    for identifier in [k for k in request.POST.keys()
                       if k.startswith("ingredient_")]:
        index = int(identifier[len("ingredient_"):])
        ingredient = Ingredient.objects.get(pk=request.POST['ingredient_' + str(index)])
        quantity = request.POST['quantity_' + str(index)]
        unit = Unit.objects.get(pk=request.POST['unit_' + str(index)])
        ingredients.append((ingredient, quantity, unit))
    
    # Sanitise the list
    ids = [i.id for i, _, _ in ingredients]
    if sorted(list(set(ids))) != sorted(ids):
        return render(request, 'kansas/edit_recipe.html', {
            'recipe': recipe,
            'ingredients': ingredients,
            'units': units,
            'error_message': "Can't have multiple instances of the same ingredient."
        })
    
    # =====
    # Nothing from here on can fail, so fine to do the updates as we go
    # =====
    # Check for deleted ingredients
    for ingredient in recipe.recipeingredient_set.all():
        if ingredient.id not in ids:
            ingredient.delete()

    # For each ingredient update the existing values or create new entries
    for ingredient, quantity, unit in ingredients:
        try:
            existing = recipe.recipeingredient_set.get(ingredient=ingredient)
            existing.quantity = quantity
            existing.unit = unit
            existing.save()
        except RecipeIngredient.DoesNotExist:
            recipe.recipeingredient_set.create(
                ingredient=ingredient,
                quantity=quantity,
                unit=unit,
            )

    recipe.display_name = request.POST.get('display_name', recipe.display_name)
    recipe.servings = request.POST.get('servings', recipe.servings)
    recipe.calories_pp = request.POST.get('calories', recipe.calories_pp)
    recipe.grams_protein_pp = request.POST.get('protein', recipe.grams_protein_pp)
    recipe.grams_carbs_pp = request.POST.get('carbs', recipe.grams_carbs_pp)
    recipe.grams_fat_pp = request.POST.get('fat', recipe.grams_fat_pp)

    recipe.save()
    return HttpResponseRedirect(reverse('kansas:recipe', args=(recipe.id,)))

def new_recipe(request):
    recipe = Recipe()
    ingredients = Ingredient.objects.all()
    units = Unit.objects.all()
    return render(request, 'kansas/edit_recipe.html', {
        'recipe': recipe,
        'ingredients': ingredients,
        'units': units,
    })

def recipe(request, recipe_id):
    recipe = get_object_or_404(Recipe, pk=recipe_id)
    ingredients = Ingredient.objects.all()
    units = Unit.objects.all()
    return render(request, 'kansas/recipe.html', {
        'recipe': recipe,
        'ingredients': ingredients,
        'units': units,
    })

@login_required
def edit_recipe(request, recipe_id):
    recipe = get_object_or_404(Recipe, pk=recipe_id)
    ingredients = Ingredient.objects.all()
    units = Unit.objects.all()
    return render(request, 'kansas/edit_recipe.html', {
        'recipe': recipe,
        'ingredients': ingredients,
        'units': units,
    })

@login_required
def save_recipe(request, recipe_id=None):
    if recipe_id is not None:
        recipe: Recipe = get_object_or_404(Recipe, pk=recipe_id)
    else:
        recipe: Recipe = Recipe.objects.create()
    return _save_recipe_from_request(recipe, request)
