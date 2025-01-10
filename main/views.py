from django.shortcuts import render
from .pokeapi import get_pokemon_by_id, get_pokemon_by_name, get_all_pokemon, get_all_pokemon_for_teams
from .pokemon import Pokemon
from django.shortcuts import render
from django.http import JsonResponse
from .battle_system import BattleSystem
import random
import json

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
    if request.headers.get('X-Requested-With') == 'XMLHttpRequest':
        # Pour les requêtes AJAX, générer et renvoyer l'équipe du bot
        bot_team_ids = random.sample(range(1, 152), 5)
        bot_team = [Pokemon(get_pokemon_by_id(id)) for id in bot_team_ids]

        # Convertir l'équipe bot en format JSON
        bot_team_data = [{
            'id': pokemon.id,
            'name': pokemon.name,
            'image': f'https://raw.githubusercontent.com/PokeAPI/sprites/master/sprites/pokemon/{pokemon.id}.png'  # Ajustez selon votre structure
        } for pokemon in bot_team]

        return JsonResponse({
            'status': 'success',
            'bot_team': bot_team_data
        })

    return render(request, 'fightclub.html')


def battle_result(request):
    if request.method == 'POST':
        data = json.loads(request.body)
        player_team_ids = [pokemon['id'] for pokemon in data['player_team']]
        bot_team_ids = [pokemon['id'] for pokemon in data['bot_team']]

        # Récupérer les Pokémon
        player_team = [Pokemon(get_pokemon_by_id(int(id))) for id in player_team_ids]
        bot_team = [Pokemon(get_pokemon_by_id(int(id))) for id in bot_team_ids]

        # Simuler les combats
        results = []
        score_player = 0
        score_bot = 0

        for p_pokemon, b_pokemon in zip(player_team, bot_team):
            battle_result = BattleSystem.simulate_battle(p_pokemon, b_pokemon)

            winner = battle_result['winner']
            if winner == p_pokemon:
                score_player += 1
            else:
                score_bot += 1

            results.append({
                'player_pokemon': {
                    'id': p_pokemon.id,
                    'name': p_pokemon.name,
                    'types': p_pokemon.types,
                    'stats': p_pokemon.stats,
                    'image': f'https://raw.githubusercontent.com/PokeAPI/sprites/master/sprites/pokemon/{p_pokemon.id}.png'
                },
                'bot_pokemon': {
                    'id': b_pokemon.id,
                    'name': b_pokemon.name,
                    'types': b_pokemon.types,
                    'stats': b_pokemon.stats,
                    'image': f'https://raw.githubusercontent.com/PokeAPI/sprites/master/sprites/pokemon/{b_pokemon.id}.png'
                },
                'winner': 'player' if winner == p_pokemon else 'bot',
                'rounds': battle_result['rounds'],
                'type_effectiveness': battle_result['type_effectiveness']
            })

        return JsonResponse({
            'status': 'success',
            'duels': results,
            'final_score': {'player': score_player, 'bot': score_bot},
            'winner': 'player' if score_player > score_bot else 'bot'
        })

    return render(request, 'battle_result.html')