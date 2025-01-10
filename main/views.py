from django.shortcuts import render
from .pokeapi import (
    get_pokemon_by_id,
    get_pokemon_by_name,
    get_all_pokemon,
    get_all_pokemon_for_teams,
)
from .pokemon import Pokemon
from django.shortcuts import render
from random import randint
import json, re
from openai import OpenAI
from django.http import JsonResponse
from django.views.decorators.csrf import csrf_exempt
from django.http import JsonResponse
import random

# gérer l'affichage de la liste des pokemons sur la page accueil
def HomeListPokemon(request):
    all = get_all_pokemon()
    return render(
        request,
        "home.html",
        {
            "all": all,
        },
    )


# gérer l'affichage des pokemons pour la gestion de l'équipe
def EquipePokemon(request):
    all = get_all_pokemon_for_teams()
    return render(
        request,
        "equipe.html",
        {
            "all": all,
        },
    )


def DetailPokemon(request, name):
    """
    Gère l'affichage des détails d'un pokemon
    Récupère les informations du pokemon via l'API PokeAPI
    Si le pokemon n'existe pas (ou si son id est supérieur à 151),
    affiche la page d'erreur 404

    Args:
        request (django.http.HttpRequest): la requête HTTP
        name (str): le nom du pokemon

    Returns:
        django.http.HttpResponse: la page HTML affichant les détails du pokemon
    """
    pokemonJson = get_pokemon_by_name(name)
    if pokemonJson is None or pokemonJson["id"] > 151:
        return render(request, "404.html")

    poke = Pokemon(pokemonJson)
    # Ajoute également les pokemon suivant et précédent pour la navigation
    pokeBefore = Pokemon(get_pokemon_by_id(poke.id - 1 if poke.id > 1 else 1))
    pokeAfter = Pokemon(get_pokemon_by_id((poke.id) % 151 + 1))

    statsList = [
        {"name": name.capitalize(), "qte": qte} for name, qte in poke.stats.items()
    ]

    return render(
        request,
        "detail.html",
        {"pokemon": poke, "before": pokeBefore, "after": pokeAfter, "stats": statsList},
    )

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

At the end, when one of the teams wins, you will tell the user that they won.

You may use **text** or *text* for abilities, moves, types, Titles to make it easier to read for the user
"""
    
    user_prompt = f"""# Here is the **user's team**:
{user_team_presentation}
# Here is the **AI's team**:
{ai_team_presentation}"""
    
    return render(request, 'aiduel.html', {'system_prompt': system_prompt, 'user_prompt': user_prompt, 'user_team': user_team, 'ai_team': ai_team})

@csrf_exempt
def ChatAPi(request):
    def battle_text_to_html(text):
        # Remplace **text** par <strong>text</strong> et *text* par <i>text</i>
        html = re.sub(r'\*\*(.*?)\*\*', r'<strong>\1</strong>', text)
        html = re.sub(r'\*(.*?)\*', r'<i>\1</i>', html)
        
        # Remplace \n par <br>
        html = html.replace('\n', '<br>')
        return html
    
    if request.method == "POST":
        try:
            data = json.loads(request.body.decode("utf-8"))
            model = data.get("model")
            base_url = data.get("baseUrl")
            api_key = data.get("apiKey")
            system_prompt = data.get("systemPrompt")
            user_prompt = data.get("userPrompt")
            
            if api_key is None or len(api_key) == 0 or api_key == "":
                api_key = "API KEYS ARE JUST SOCIAL CONSTUCTS"          

            if not all([model, base_url, api_key, system_prompt, user_prompt]):
                return JsonResponse({"error": "Missing required fields"}, status=400)
            
            client = OpenAI(
                base_url=base_url,
                api_key=api_key,
            )

            response = client.chat.completions.create(
                model=model,
                messages=[
                    {"role": "system", "content": system_prompt},
                    {"role": "user", "content": user_prompt},
                ],
            )

            return JsonResponse({"message": battle_text_to_html(response.choices[0].message.content)}, status=200, safe=False)
        
        except json.JSONDecodeError:
            return JsonResponse({"error": "Invalid JSON data"}, status=400)
        except Exception as e:
            return JsonResponse({"error": str(e)}, status=500)
    else:
        return JsonResponse({"error": "Only POST method is allowed"}, status=405)