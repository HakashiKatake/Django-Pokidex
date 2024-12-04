import requests
from django.shortcuts import render

import requests
import math
import random

import requests
from django.shortcuts import render
import random

def home(request):
    base_url = "https://pokeapi.co/api/v2/"
    context = {}

    # Get region (Gen 1, Gen 2, etc.) from GET params
    region = request.GET.get('region', '1')

    # Get search query from GET params
    search_query = request.GET.get('search', '').lower()

    # Fetch Pokémon based on region (Gen 1, Gen 2)
    offset = (int(region) - 1) * 151  # each region has 151 Pokémon
    limit = 151  # Gen 1, Gen 2, etc. have 151 Pokémon each

    pokemon_list_url = f"{base_url}pokemon?offset={offset}&limit={limit}"
    response = requests.get(pokemon_list_url)

    if response.status_code == 200:
        data = response.json()
        pokemons = data['results']

        # If search query is present, filter Pokémon names
        if search_query:
            pokemons = [pokemon for pokemon in pokemons if search_query in pokemon['name'].lower()]

        context['pokemons'] = pokemons

        # Adding image URL for each Pokémon
        for pokemon in context['pokemons']:
            pokemon_id = pokemon['url'].split('/')[-2]
            pokemon['image_url'] = f"https://raw.githubusercontent.com/PokeAPI/sprites/master/sprites/pokemon/other/official-artwork/{pokemon_id}.png"

        # Random Pokémon feature
        if context['pokemons']:
            random_pokemon = random.choice(context['pokemons'])
            context['random_pokemon'] = random_pokemon

    # Add regions to the context for the dropdown menu
    context['regions'] = [
        {'id': 1, 'name': 'Gen 1'},
        {'id': 2, 'name': 'Gen 2'},
        {'id': 3, 'name': 'Gen 3'},
        {'id': 4, 'name': 'Gen 4'},
        {'id': 5, 'name': 'Gen 5'},
        {'id': 6, 'name': 'Gen 6'},
        {'id': 7, 'name': 'Gen 7'},
        # Add more regions as needed
    ]

    return render(request, 'home.html', context)




def pokemon_details(request, pokemon_name):
    base_url = "https://pokeapi.co/api/v2/"
    context = {}

    # Fetch Pokémon data
    pokemon_url = f"{base_url}pokemon/{pokemon_name.lower()}/"
    response = requests.get(pokemon_url)

    if response.status_code == 200:
        data = response.json()
        context['pokemon'] = {
            'name': data['name'],
            'image': data['sprites']['front_default'],
            'types': [t['type']['name'] for t in data['types']],
            'abilities': [a['ability']['name'] for a in data['abilities']],
            'stats': {stat['stat']['name']: stat['base_stat'] for stat in data['stats']},
            'weight': data['weight'],
            'height': data['height'],
            'moves': [move['move']['name'] for move in data['moves']],
        }

        # Fetch Evolution Chain
        species_url = data['species']['url']
        species_response = requests.get(species_url)

        if species_response.status_code == 200:
            species_data = species_response.json()
            evolution_chain_url = species_data['evolution_chain']['url']
            evolution_response = requests.get(evolution_chain_url)

            if evolution_response.status_code == 200:
                evolution_data = evolution_response.json()
                chain = evolution_data['chain']
                evolution_list = []

                while chain:
                    evolution_list.append({
                        'name': chain['species']['name'],
                        'image': f"https://raw.githubusercontent.com/PokeAPI/sprites/master/sprites/pokemon/other/official-artwork/{chain['species']['url'].split('/')[-2]}.png"
                    })
                    chain = chain['evolves_to'][0] if chain['evolves_to'] else None

                context['pokemon']['evolution'] = evolution_list
    else:
        context['error'] = "Pokémon not found!"

    return render(request, 'details.html', context)

def pokemon_list(request):
    base_url = "https://pokeapi.co/api/v2/pokemon"
    page = int(request.GET.get('page', 1))  # Default to page 1
    limit = 20  # Number of Pokémon per page
    offset = (page - 1) * limit  # Calculate offset for API
    response = requests.get(f"{base_url}?limit={limit}&offset={offset}")

    context = {}
    if response.status_code == 200:
        data = response.json()
        context['pokemon_list'] = data['results']
        context['page'] = page
        context['total_pages'] = math.ceil(data['count'] / limit)
    return render(request, 'pokemon_list.html', context)



def random_pokemon(request):
    random_id = random.randint(1, 898)  # Assuming 898 Pokémon
    url = f"https://pokeapi.co/api/v2/pokemon/{random_id}/"
    response = requests.get(url)
    context = {}

    if response.status_code == 200:
        data = response.json()
        context['pokemon'] = {
            'name': data['name'],
            'image': data['sprites']['front_default'],
            'types': [t['type']['name'] for t in data['types']],
        }
    return render(request, 'home.html', context)
