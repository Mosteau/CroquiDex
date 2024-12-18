from django.shortcuts import render
from .pokeapi import get_pokemon_by_id, get_pokemon_by_name
from .pokemon import Pokemon

# Create your views here.
def HomeListPokemon(request):
    
    test = get_pokemon_by_id(25)
    
    return render(request, 'home.html', {'pokemon': str(test)})

def EquipePokemon(request):
    return render(request, 'equipe.html')

def DetailPokemon(request, name):
    pokemonJson = get_pokemon_by_name(name)
    poke = Pokemon(pokemonJson)
    pokeBefore = Pokemon(get_pokemon_by_id(poke.id - 1 if poke.id > 1 else 1))
    pokeAfter = Pokemon(get_pokemon_by_id((poke.id + 1)%151))

    statsList = [{'name': name.capitalize(), 'qte': qte} for name, qte in poke.stats.items()]
    
    return render(request, 'detail.html', {'pokemon': poke, 'before': pokeBefore, 'after': pokeAfter, 'stats': statsList})

def FightClubPokemon(request):
    return render(request, 'fightclub.html')
