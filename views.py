from django.contrib.auth.decorators import login_required
from django.http import HttpResponse, HttpResponseRedirect
from django.shortcuts import get_object_or_404, render
from django.urls import reverse

from .models import Recipe, Ingredient, RecipeIngredient, Unit

def index(request):
    recipes_list = Recipe.objects.all()
    context = {
        'recipes_list': recipes_list,
    }
    return render(request, 'kansas/index.html', context)

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
def save_recipe(request, recipe_id):
    recipe: Recipe = get_object_or_404(Recipe, pk=recipe_id)

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
    recipe.calories_pp = request.POST.get('calores', recipe.calories_pp)
    recipe.grams_protein_pp = request.POST.get('protein', recipe.grams_protein_pp)
    recipe.grams_carbs_pp = request.POST.get('carbs', recipe.grams_carbs_pp)
    recipe.grams_fat_pp = request.POST.get('fat', recipe.grams_fat_pp)
    recipe.grams_fibre_pp = request.POST.get('fibre', recipe.grams_fibre_pp)

    recipe.save()
    return HttpResponseRedirect(reverse('kansas:recipe', args=(recipe_id,)))
