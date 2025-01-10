class BattleSystem:
    @staticmethod
    def calculate_type_advantage(attacker_types, defender_types):
        type_chart = {
            'normal': {
                'rock': 0.5,
                'ghost': 0,
                'steel': 0.5
            },
            'fire': {
                'fire': 0.5,
                'water': 0.5,
                'grass': 2.0,
                'ice': 2.0,
                'bug': 2.0,
                'rock': 0.5,
                'dragon': 0.5,
                'steel': 2.0
            },
            'water': {
                'fire': 2.0,
                'water': 0.5,
                'grass': 0.5,
                'ground': 2.0,
                'rock': 2.0,
                'dragon': 0.5
            },
            'electric': {
                'water': 2.0,
                'electric': 0.5,
                'grass': 0.5,
                'ground': 0,
                'flying': 2.0,
                'dragon': 0.5
            },
            'grass': {
                'fire': 0.5,
                'water': 2.0,
                'grass': 0.5,
                'poison': 0.5,
                'ground': 2.0,
                'flying': 0.5,
                'bug': 0.5,
                'rock': 2.0,
                'dragon': 0.5,
                'steel': 0.5
            },
            'ice': {
                'fire': 0.5,
                'water': 0.5,
                'grass': 2.0,
                'ice': 0.5,
                'ground': 2.0,
                'flying': 2.0,
                'dragon': 2.0,
                'steel': 0.5
            },
            'fighting': {
                'normal': 2.0,
                'ice': 2.0,
                'poison': 0.5,
                'flying': 0.5,
                'psychic': 0.5,
                'bug': 0.5,
                'rock': 2.0,
                'ghost': 0,
                'dark': 2.0,
                'steel': 2.0
            },
            'poison': {
                'grass': 2.0,
                'poison': 0.5,
                'ground': 0.5,
                'rock': 0.5,
                'ghost': 0.5,
                'steel': 0
            },
            'ground': {
                'fire': 2.0,
                'electric': 2.0,
                'grass': 0.5,
                'poison': 2.0,
                'flying': 0,
                'bug': 0.5,
                'rock': 2.0,
                'steel': 2.0
            },
            'flying': {
                'electric': 0.5,
                'grass': 2.0,
                'fighting': 2.0,
                'bug': 2.0,
                'rock': 0.5,
                'steel': 0.5
            },
            'psychic': {
                'fighting': 2.0,
                'poison': 2.0,
                'psychic': 0.5,
                'dark': 0,
                'steel': 0.5
            },
            'bug': {
                'fire': 0.5,
                'grass': 2.0,
                'fighting': 0.5,
                'poison': 0.5,
                'flying': 0.5,
                'psychic': 2.0,
                'ghost': 0.5,
                'dark': 2.0,
                'steel': 0.5
            },
            'rock': {
                'fire': 2.0,
                'ice': 2.0,
                'fighting': 0.5,
                'ground': 0.5,
                'flying': 2.0,
                'bug': 2.0,
                'steel': 0.5
            },
            'ghost': {
                'normal': 0,
                'psychic': 2.0,
                'ghost': 2.0,
                'dark': 0.5
            },
            'dragon': {
                'dragon': 2.0,
                'steel': 0.5
            },
            'steel': {
                'fire': 0.5,
                'water': 0.5,
                'electric': 0.5,
                'ice': 2.0,
                'rock': 2.0,
                'steel': 0.5
            },
            'dark': {
                'fighting': 0.5,
                'psychic': 2.0,
                'ghost': 2.0,
                'dark': 0.5
            }
        }

        multiplier = 1.0
        for att_type in attacker_types:
            for def_type in defender_types:
                if att_type in type_chart and def_type in type_chart[att_type]:
                    multiplier *= type_chart[att_type][def_type]

        return multiplier

    @staticmethod
    def calculate_pokemon_power(pokemon, opponent):
        base_power = (
                pokemon.stats['attack'] * 0.4 +
                pokemon.stats['defense'] * 0.3 +
                pokemon.stats['hp'] * 0.2 +
                pokemon.stats['speed'] * 0.1
        )

        type_multiplier = BattleSystem.calculate_type_advantage(pokemon.types, opponent.types)
        return base_power * type_multiplier

    @staticmethod
    def simulate_battle(pokemon1, pokemon2):
        hp1 = pokemon1.stats['hp']
        hp2 = pokemon2.stats['hp']

        first = pokemon1 if pokemon1.stats['speed'] > pokemon2.stats['speed'] else pokemon2
        second = pokemon2 if first == pokemon1 else pokemon1

        rounds = []

        while hp1 > 0 and hp2 > 0:
            # Premier attaquant
            power1 = BattleSystem.calculate_pokemon_power(first, second)
            if first == pokemon1:
                hp2 -= power1
            else:
                hp1 -= power1

            if hp1 > 0 and hp2 > 0:
                power2 = BattleSystem.calculate_pokemon_power(second, first)
                if second == pokemon1:
                    hp2 -= power2
                else:
                    hp1 -= power2

            rounds.append({
                'hp1': max(0, hp1),
                'hp2': max(0, hp2),
                'first_attacker': first.name,
                'second_attacker': second.name
            })

        winner = pokemon1 if hp1 > 0 else pokemon2
        return {
            'winner': winner,
            'rounds': rounds,
            'remaining_hp': max(0, hp1) if winner == pokemon1 else max(0, hp2),
            'type_effectiveness': BattleSystem.calculate_type_advantage(winner.types, (
                pokemon2 if winner == pokemon1 else pokemon1).types)
        }