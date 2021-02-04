from django.urls import path

from . import views

app_name = 'kansas'
urlpatterns = [
    path('', views.index, name='index'),
    path('week/', views.week, name='week'),
    path('recipe/new/', views.new_recipe, name='new_recipe'),
    path('recipe/<int:recipe_id>/', views.recipe, name='recipe'),
    path('recipe/<int:recipe_id>/edit/', views.edit_recipe, name='edit_recipe'),
    path('recipe/<int:recipe_id>/save/', views.save_recipe, name='save_recipe'),
    path('recipe/new/save/', views.save_recipe, name='save_new_recipe'),
]