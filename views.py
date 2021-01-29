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

def add_ingredient(request, recipe_id):
    recipe = get_object_or_404(Recipe, pk=recipe_id)
    ingredients = Ingredient.objects.all()
    units = Unit.objects.all()
    try:
        selected_ingredient = Ingredient.objects.get(pk=request.POST['ingredient'])
    except (KeyError, Recipe.DoesNotExist) as e:
        print(e)
        return render(request, 'kansas/recipe.html', {
            'recipe': recipe,
            'ingredients': ingredients,
            'units': units,
            'error_message': "Invalid ingredient selected."
        })

    try:
        selected_unit = Unit.objects.get(pk=request.POST['unit'])
    except (KeyError, Recipe.DoesNotExist) as e:
        print(e)
        return render(request, 'kansas/recipe.html', {
            'recipe': recipe,
            'ingredients': ingredients,
            'units': units,
            'error_message': "Invalid unit selected."
        })

    try:
        quantity = float(request.POST['quantity'])
    except (KeyError, ValueError) as e:
        print(e)
        return render(request, 'kansas/recipe.html', {
            'recipe': recipe,
            'ingredients': ingredients,
            'units': units,
            'error_message': "Invalid quantity specified."
        })

    RecipeIngredient.objects.create(ingredient=selected_ingredient,
                                    recipe=recipe,
                                    quantity=quantity,
                                    unit=selected_unit)
    return HttpResponseRedirect(reverse('kansas:recipe', args=(recipe_id,)))