from django.urls import path

from . import views

app_name = 'kansas'
urlpatterns = [
    path('', views.index, name='index'),
    path('recipe/<int:recipe_id>/', views.recipe, name='recipe'),
    path('recipe/<int:recipe_id>/add_ingredient/', views.add_ingredient, name='add_ingredient'),
]