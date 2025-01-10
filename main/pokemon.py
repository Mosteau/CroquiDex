class Pokemon:
    def __init__(self, data):
        """
        Initialisation d'un Pokemon

        Args:
            data (dict): Les données du Pokemon provenant de la PokeAPI
        """
        self.id = data.get("id")
        self.name = data.get("name")

        self.types = [t["type"]["name"] for t in data.get("types", [])]

        self.abilities = [a["ability"]["name"] for a in data.get("abilities", [])]

        self.stats = {
            stat["stat"]["name"]: stat["base_stat"] for stat in data.get("stats", [])
        }

        self.base_experience = data.get("base_experience")

        # La formule pour calculer le poids est la suivante :
        # si le poids est supérieur à1 (en kg), on le multiplie par 0,1 (soit 100g) et on l'affiche en kg
        # sinon, on le multiplie par 100 et on l'affiche en grammes
        self.weight = (
            str(int(data.get("weight")) * 0.1) + " kg"
            if data.get("weight") > 1
            else str(int(data.get("weight")) * 100) + " g"
        )

        # On multiplie la taille par 10 pour passer de décimétres à cm
        self.height = str(int(data.get("height")) * 10) + " cm"

        self.sprites = data.get("sprites", {})

        self.cries = data.get("cries", {})

    def __repr__(self):
        """Présente le pokemon (pour la console)

        Returns:
            str: Description du pokemon
        """
        return (
            f"Pokemon(id={self.id}, name='{self.name}', types={self.types}, "
            f"abilities={self.abilities}, stats={self.stats}, "
            f"base_experience={self.base_experience}, "
            f"weight={self.weight}, height={self.height}"
            f"sprites={list(self.sprites.keys())}"
            f"cries={list(self.cries.keys())})"
        )
    
    def presentation(self):
        return (
            f"{self.name.capitalize()} is a pokemon of types {self.types}.\n"
            f"They have the following abilities: {self.abilities}.\n"
            f"Their stats are: {self.stats}.\n"
            f"They weight {self.weight} for a height of {self.height}."
        )