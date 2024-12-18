from django.shortcuts import render
from .pokeapi import get_pokemon_by_id

# Create your views here.
def HomeListPokemon(request):
    
    test = get_pokemon_by_id(25)
    
    return render(request, 'home.html', {'pokemon': str(test)})

from django.shortcuts import render
from .pokeapi import get_pokemon_by_id

# Create your views here.
def HomeListPokemon(request):
    
    test = get_pokemon_by_id(25)
    
    return render(request, 'home.html', {'pokemon': str(test)})

def EquipePokemon(request):
    # Récupérer les 151 premiers Pokémon
    pokemons = []
    for pokemon_id in range(1, 151):
        pokemon = get_pokemon_by_id(pokemon_id)
        if pokemon:
            pokemons.append({
                'id': pokemon['id'],
                'name': pokemon['name'].capitalize(),
                'image': pokemon['sprites']['front_default']
            })
    
    return render(request, 'equipe.html', {'pokemons': pokemons})

def DetailPokemon(request):
    return render(request, 'detail.html')

def FightClubPokemon(request):
    return render(request, 'fightclub.html')

