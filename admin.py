from django.contrib import admin

from .models import Unit, Ingredient, Recipe

admin.site.register(Unit)
admin.site.register(Ingredient)
admin.site.register(Recipe)