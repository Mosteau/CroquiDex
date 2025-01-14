from .pokeapi import get_pokemon_by_id
from .pokemon import Pokemon

def systemPrompt():
    return """You're the **best** Pokemon battle teller of the world and you have to write a **cool battle** between the user's team and the AI's team. You will be presented their pokemon with their stats and you will be asked to **write a description of the battle**.

The battle must be **epic** with **lots of details and plot twists**. The battle must be **realistic** (take in account the stats of the pokemon and their types).

At the end, when one of the teams wins, you will tell the user that they won.

You may use **text** or *text* for abilities, moves, types, Titles to make it easier to read for the user
"""

def userPrompt(user_team_ids, ai_team_ids):
    user_team_presentation = ''
    for pokemon_id in user_team_ids:
        pokemon = Pokemon(get_pokemon_by_id(pokemon_id))
        user_team_presentation += pokemon.presentation() + '\n\n'

    ai_team_presentation = ''
    for pokemon_id in ai_team_ids:
        pokemon = Pokemon(get_pokemon_by_id(pokemon_id))
        ai_team_presentation += pokemon.presentation() + '\n\n'

    return f"""# Here is the **user's team**:\n{user_team_presentation}\n\n# Here is the **AI's team**:\n{ai_team_presentation}"""

if __name__ == '__main__':
    print(userPrompt([14, 27, 30, 7, 10], [14, 27, 30, 7, 10]))