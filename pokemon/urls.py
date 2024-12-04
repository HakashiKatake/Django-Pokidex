from django.urls import path
from . import views

urlpatterns = [
    path('', views.home, name='home'),
    path('pokemon/<str:pokemon_name>/', views.pokemon_details, name='pokemon_details'),
    path('pokemon-list/', views.pokemon_list, name='pokemon_list'),
    path('random/', views.random_pokemon, name='random_pokemon'),


]

