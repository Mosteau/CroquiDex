import requests

BASE_URL = "https://pokeapi.co/api/v2/"

def get_pokemon_by_id(pokemon_id: int) -> dict:
    """
    Renvoie les informations d'un pokemon par son id

    Args:
      pokemon_id (int): l'id du pokemon

    Returns:
      dict : un dictionnaire contenant les informations du pokemon
    """

    response = requests.get(f"{BASE_URL}pokemon/{pokemon_id}")
    if response.status_code == 200:
        return response.json()
    else:
        return None


def get_pokemon_by_name(pokemon_name):
    """Récupère les informations d'un Pokémon par son nom.

    Args:
        pokemon_name (str): Le nom du Pokémon.

    Returns:
        dict: Un dictionnaire contenant les informations du Pokémon si la requête est réussie, sinon None.
    """
    response = requests.get(f"{BASE_URL}pokemon/{pokemon_name.lower()}")
    if response.status_code == 200:
        return response.json()
    else:
        return None


def get_pokemon_ability(ability_id):
    """
    Renvoie les informations d'une capacité d'un pokemon par son id

    Args:
        ability_id (int): l'id de la capacité

    Returns:
        dict : un dictionnaire contenant les informations de la capacité si la requête est réussie, sinon None
    """
    response = requests.get(f"{BASE_URL}ability/{ability_id}")
    if response.status_code == 200:
        return response.json()
    else:
        return None


def get_pokemon_type(type_id: int) -> dict:
    """
    Renvoie les informations d'un type de pokemon par son id

    Args:
        type_id (int): l'id du type

    Returns:
        dict: Un dictionnaire contenant les informations du type si la requête est réussie, sinon None
    """
    response = requests.get(f"{BASE_URL}type/{type_id}")
    if response.status_code == 200:
        return response.json()
    else:
        return None


def get_all_pokemon():
    """
    Récupère tous les Pokémon pour la page d'accueil.

    Effectue une requête à l'API PokeAPI pour obtenir une liste de Pokémon avec leurs images.

    Returns:
        list: Une liste contenant des paires de noms de Pokémon et leurs URLs d'images si la requête est réussie, sinon None.
    """
    response = requests.get(f"{BASE_URL}pokemon?limit=151")

    pokemon_with_imgs = []

    if response.status_code == 200:
        for i, pokemon in enumerate(response.json()["results"]):
            pokemon_with_imgs.append(
                [
                    pokemon["name"],
                    f"https://raw.githubusercontent.com/PokeAPI/sprites/master/sprites/pokemon/{i+1}.png",
                ]
            )

        return pokemon_with_imgs
    else:
        return None


def get_all_pokemon_for_teams():
    """
    Récupère tous les Pokémon pour la page de gestion de l'équipe.

    Effectue une requête à l'API PokeAPI pour obtenir une liste de Pokémon avec leurs images.

    Returns:
        list: Une liste contenant des paires de noms de Pokémon et leurs URLs d'images si la requête est réussie, sinon None.
    """
    response = requests.get(f"{BASE_URL}pokemon?limit=151")

    pokemon_with_imgs = []

    if response.status_code == 200:
        for i, pokemon in enumerate(response.json()["results"]):
            pokemon_with_imgs.append(
                {
                    "id": str(i + 1),
                    "name": pokemon["name"],
                    "image": f"https://raw.githubusercontent.com/PokeAPI/sprites/master/sprites/pokemon/{i+1}.png",
                }
            )

        return pokemon_with_imgs
    else:
        return None
