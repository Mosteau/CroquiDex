from django.test import TestCase
from .pokeapi import get_pokemon_by_id, get_pokemon_by_name, get_all_pokemon
from .pokemon import Pokemon

class PokeAPITest(TestCase):

    def test_get_pokemon_by_id(self):
        """get_pokemon_by_id should return a pokemon with the given id"""
        pokemon = get_pokemon_by_id(1)
        self.assertEqual(pokemon['name'], 'bulbasaur')
        self.assertEqual(pokemon['id'], 1)

    def test_get_pokemon_by_name(self):
        """get_pokemon_by_name should return a pokemon with the given name"""
        pokemon = get_pokemon_by_name('charmander')
        self.assertEqual(pokemon['name'], 'charmander')
        self.assertEqual(pokemon['id'], 4)
        
    def test_get_pokemon_by_name_should_return_none_if_does_not_exist(self):
        """get_pokemon_by_name should return None if the pokemon does not exist"""
        pokemon = get_pokemon_by_name('pikachu-2')
        self.assertIsNone(pokemon)
        
    def test_get_pokemon_by_id_should_return_none_if_does_not_exist(self):
        """get_pokemon_by_id should return None if the pokemon does not exist"""
        pokemon = get_pokemon_by_id(0)
        self.assertIsNone(pokemon)

    def test_get_all_pokemon(self):
        """get_all_pokemon should return a list of all pokemon"""
        pokemon = get_all_pokemon()
        self.assertEqual(len(pokemon), 151)

class PokemonTest(TestCase):
    def test_pokemon(self):
        pokemon = get_pokemon_by_id(1)
        poke = Pokemon(pokemon)
        self.assertEqual(poke.id, 1)
        self.assertEqual(poke.name, 'bulbasaur')
        self.assertEqual(poke.types, ['grass', 'poison'])
        self.assertEqual(poke.abilities, ['overgrow', 'chlorophyll'])
        self.assertEqual(poke.stats, {'hp': 45, 'attack': 49, 'defense': 49, 'special-attack': 65, 'special-defense': 65, 'speed': 45})
        self.assertEqual(poke.base_experience, 64)
        self.assertEqual(poke.weight, '6.9 kg')
        self.assertEqual(poke.height, '70 cm')