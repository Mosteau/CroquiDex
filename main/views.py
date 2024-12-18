from django.shortcuts import render
from .pokeapi import get_pokemon_by_id, get_pokemon_by_name

# Create your views here.
def HomeListPokemon(request):
    
    test = get_pokemon_by_id(25)
    
    return render(request, 'home.html', {'pokemon': str(test)})

def EquipePokemon(request):
    return render(request, 'equipe.html')

def DetailPokemon(request, name):
    pokemon = get_pokemon_by_name(name)
    return render(request, 'detail.html', {'pokemon': pokemon})

def FightClubPokemon(request):
    return render(request, 'fightclub.html')
