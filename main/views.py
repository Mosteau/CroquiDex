from django.shortcuts import render

# Create your views here.
def HomeListPokemon(request):
    return render(request, 'home.html')

def EquipePokemon(request):
    return render(request, 'equipe.html')

def DetailPokemon(request):
    return render(request, 'detail.html')

def FightClubPokemon(request):
    return render(request, 'fightclub.html')
