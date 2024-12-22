from django.shortcuts import render
from .pokeapi import get_pokemon_by_id, get_pokemon_by_name, get_all_pokemon, get_all_pokemon_for_teams
from .pokemon import Pokemon
from django.shortcuts import render
from .pokeapi import get_pokemon_by_id
from random import randint

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

def AIDuel(request):
    # userTeam = [get_pokemon_by_id(i) for i in request.session['userTeam']]
    user_team = [Pokemon(get_pokemon_by_id(i)) for i in [14, 27, 30, 7, 10]]
    ai_team = [Pokemon(get_pokemon_by_id(randint(1, 151))) for _ in range(5)]
    
    user_team_presentation = ''
    for pokemon in user_team:
        user_team_presentation += pokemon.presentation() + '\n\n'
    
    ai_team_presentation = ''
    for pokemon in ai_team:
        ai_team_presentation += pokemon.presentation() + '\n\n'
    
    system_prompt = """You're the **best** Pokemon battle teller of the world and you have to write a **cool battle** between the user's team and the AI's team. You will be presented their pokemon with their stats and you will be asked to **write a description of the battle**.

The battle must be **epic** with **lots of details and plot twists**. The battle must be **realistic** (take in account the stats of the pokemon and their types).

At the end, when one of the teams wins, you will tell the user that they won. Your answer must always end with either "USER" or "AI".
"""
    
    user_prompt = f"""# Here is the **user's team**:
{user_team_presentation}
# Here is the **AI's team**:
{ai_team_presentation}"""
    
    return render(request, 'aiduel.html', {'system_prompt': system_prompt, 'user_prompt': user_prompt, 'user_team': user_team, 'ai_team': ai_team})

