from django.test import TestCase
from .pokeapi import get_pokemon_by_id, get_pokemon_by_name

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
