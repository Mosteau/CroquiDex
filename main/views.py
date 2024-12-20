from django.shortcuts import render
from .pokeapi import get_pokemon_by_id, get_pokemon_by_name, get_all_pokemon
from .pokemon import Pokemon

# Create your views here.
def HomeListPokemon(request):
    
    test = get_pokemon_by_id(25)
    
    return render(request, 'home.html', {'pokemon': str(test)})

from django.shortcuts import render
from .pokeapi import get_pokemon_by_id

# Create your views here.
def HomeListPokemon(request):
    all = get_all_pokemon()
    
    return render(request, 'home.html', {'all': all,})

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

def DetailPokemon(request, name):
    pokemonJson = get_pokemon_by_name(name)
    
    if pokemonJson is None or pokemonJson["id"] > 151:
        return render(request, '404.html')
    
    poke = Pokemon(pokemonJson)
    pokeBefore = Pokemon(get_pokemon_by_id(poke.id - 1 if poke.id > 1 else 1))
    pokeAfter = Pokemon(get_pokemon_by_id((poke.id)%151 + 1))

    statsList = [{'name': name.capitalize(), 'qte': qte} for name, qte in poke.stats.items()]
    
    return render(request, 'detail.html', {'pokemon': poke, 'before': pokeBefore, 'after': pokeAfter, 'stats': statsList})

def FightClubPokemon(request):
    return render(request, 'fightclub.html')

