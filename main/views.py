from django.shortcuts import render
from .pokeapi import get_pokemon_by_id, get_pokemon_by_name, get_all_pokemon, get_all_pokemon_for_teams
from .pokemon import Pokemon
from django.shortcuts import render
from django.http import JsonResponse
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
        print(request)

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
        try:
            data = json.loads(request.body)
            player_team_ids = [pokemon['id'] for pokemon in data['player_team']]
            bot_team_ids = [pokemon['id'] for pokemon in data['bot_team']]

            # Récupérer les détails des Pokémon
            player_team = [Pokemon(get_pokemon_by_id(int(id))) for id in player_team_ids]
            bot_team = [Pokemon(get_pokemon_by_id(int(id))) for id in bot_team_ids]

            results = []
            score_player = 0
            score_bot = 0

            for p_pokemon, b_pokemon in zip(player_team, bot_team):
                # Calculer les scores pour chaque stat
                player_score = (
                        p_pokemon.stats['hp'] +
                        p_pokemon.stats['attack'] +
                        p_pokemon.stats['defense'] +
                        p_pokemon.base_experience +
                        int(float(p_pokemon.weight.split()[0])) +  # Convertir "100.0 kg" en nombre
                        int(float(p_pokemon.height.split()[0]))  # Convertir "200 cm" en nombre
                )

                bot_score = (
                        b_pokemon.stats['hp'] +
                        b_pokemon.stats['attack'] +
                        b_pokemon.stats['defense'] +
                        b_pokemon.base_experience +
                        int(float(b_pokemon.weight.split()[0])) +
                        int(float(b_pokemon.height.split()[0]))
                )

                # Déterminer le vainqueur
                winner = 'player' if player_score > bot_score else 'bot'
                if winner == 'player':
                    score_player += 1
                else:
                    score_bot += 1

                # Stocker les détails du duel
                duel = {
                    'player_pokemon': {
                        'id': p_pokemon.id,
                        'name': p_pokemon.name,
                        'types': p_pokemon.types,
                        'abilities': p_pokemon.abilities,
                        'stats': {
                            'hp': p_pokemon.stats['hp'],
                            'attack': p_pokemon.stats['attack'],
                            'defense': p_pokemon.stats['defense'],
                            'special-attack': p_pokemon.stats['special-attack'],
                            'special-defense': p_pokemon.stats['special-defense'],
                            'speed': p_pokemon.stats['speed'],
                            'experience': p_pokemon.base_experience,
                            'weight': p_pokemon.weight,
                            'height': p_pokemon.height
                        },
                        'total_score': player_score
                    },
                    'bot_pokemon': {
                        'id': b_pokemon.id,
                        'name': b_pokemon.name,
                        'types': b_pokemon.types,
                        'abilities': b_pokemon.abilities,
                        'stats': {
                            'hp': b_pokemon.stats['hp'],
                            'attack': b_pokemon.stats['attack'],
                            'defense': b_pokemon.stats['defense'],
                            'special-attack': b_pokemon.stats['special-attack'],
                            'special-defense': b_pokemon.stats['special-defense'],
                            'speed': b_pokemon.stats['speed'],
                            'experience': b_pokemon.base_experience,
                            'weight': b_pokemon.weight,
                            'height': b_pokemon.height
                        },
                        'total_score': bot_score
                    },
                    'winner': winner
                }
                results.append(duel)

            return JsonResponse({
                'status': 'success',
                'duels': results,
                'final_score': {
                    'player': score_player,
                    'bot': score_bot
                },
                'winner': 'player' if score_player > score_bot else 'bot'
            })
        except json.JSONDecodeError:
            return JsonResponse({'status': 'error', 'message': 'Invalid JSON'}, status=400)

    return render(request, 'battle_result.html')