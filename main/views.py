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
    poke.id
    pokeBefore = get_pokemon_by_id(poke.id + 1 if poke.id > 0 else 0)
    pokeAfter = get_pokemon_by_id((poke.id + 1)%151)
    
    return render(request, 'detail.html', {'pokemon': pokemonJson, 'before': pokeBefore, 'after': pokeAfter})

def FightClubPokemon(request):
    return render(request, 'fightclub.html')
