from django.shortcuts import render
from .pokeapi import get_pokemon_by_id

# Create your views here.
def HomeListPokemon(request):
    
    test = get_pokemon_by_id(25)
    
    return render(request, 'home.html', {'pokemon': str(test)})

def EquipePokemon(request):
    return render(request, 'equipe.html')

def DetailPokemon(request):
    return render(request, 'detail.html')

def FightClubPokemon(request):
    return render(request, 'fightclub.html')
