import requests

BASE_URL = "https://pokeapi.co/api/v2/"

# fonction pour récupérer un pokemon par son id
def get_pokemon_by_id(pokemon_id):
  response = requests.get(f"{BASE_URL}pokemon/{pokemon_id}")
  if response.status_code == 200:
    return response.json()
  else:
    return None

# fonction pour récupérer un pokemon par son nom
def get_pokemon_by_name(pokemon_name):
  response = requests.get(f"{BASE_URL}pokemon/{pokemon_name.lower()}")
  if response.status_code == 200:
    return response.json()
  else:
    return None
  
# fonction pour récupérer les détails d'un pokemon par son id
def get_pokemon_ability(ability_id):
  response = requests.get(f"{BASE_URL}ability/{ability_id}")
  if response.status_code == 200:
    return response.json()
  else:
    return None
# fonction pour récupérer les détails d'un pokemon par son id
def get_pokemon_type(type_id):
  response = requests.get(f"{BASE_URL}type/{type_id}")
  if response.status_code == 200:
    return response.json()
  else:
    return None

# fonction pour récupérer tous les pokemons pour la page d'accueil
def get_all_pokemon():
  response = requests.get(f"{BASE_URL}pokemon?limit=151")
  
  pokemon_with_imgs = []
  
  if response.status_code == 200:
    for i, pokemon in enumerate(response.json()["results"]):
      pokemon_with_imgs.append([pokemon["name"], f"https://raw.githubusercontent.com/PokeAPI/sprites/master/sprites/pokemon/{i+1}.png"])
    
    return pokemon_with_imgs
  else:
    return None
  
# fonction pour récupérer tous les pokemons pour la page de gestion de l'équipe
def get_all_pokemon_for_teams():
  response = requests.get(f"{BASE_URL}pokemon?limit=151")
    
  pokemon_with_imgs = []
    
  if response.status_code == 200:
      for i, pokemon in enumerate(response.json()["results"]):
          pokemon_with_imgs.append({
              'id': str(i + 1),
              'name': pokemon["name"],
              'image': f"https://raw.githubusercontent.com/PokeAPI/sprites/master/sprites/pokemon/{i+1}.png"
          })
        
      return pokemon_with_imgs
  else:
      return None