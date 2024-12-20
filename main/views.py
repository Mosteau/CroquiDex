from django.shortcuts import render
from .pokeapi import get_pokemon_by_id, get_pokemon_by_name, get_all_pokemon, get_all_pokemon_for_teams
from .pokemon import Pokemon
from django.shortcuts import render
from .pokeapi import get_pokemon_by_id

# gérer l'affichage de la liste des pokemons sur la page accueil
def HomeListPokemon(request):
    all = get_all_pokemon()
    return render(request, 'home.html', {'all': all,})

# gérer l'affichage des pokemons pour la gestion de l'équipe
def EquipePokemon(request):
    all = get_all_pokemon_for_teams()
    return render(request, 'equipe.html', {'all': all,})


# gérer l'affichage des détails d'un pokemon
def DetailPokemon(request, name):
    pokemonJson = get_pokemon_by_name(name)
    if pokemonJson is None or pokemonJson["id"] > 151:
        return render(request, '404.html')
    
    poke = Pokemon(pokemonJson)
    pokeBefore = Pokemon(get_pokemon_by_id(poke.id - 1 if poke.id > 1 else 1))
    pokeAfter = Pokemon(get_pokemon_by_id((poke.id)%151 + 1))

    statsList = [{'name': name.capitalize(), 'qte': qte} for name, qte in poke.stats.items()]
    
    return render(request, 'detail.html', {'pokemon': poke, 'before': pokeBefore, 'after': pokeAfter, 'stats': statsList})

# gérer l'affichage des pokemons de la page de combat
def FightClubPokemon(request):
    return render(request, 'fightclub.html')

