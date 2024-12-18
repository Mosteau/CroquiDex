class Pokemon:
    def __init__(self, data):
        self.id = data.get("id")
        self.name = data.get("name")

        self.types = [t["type"]["name"] for t in data.get("types", [])]

        self.abilities = [a["ability"]["name"] for a in data.get("abilities", [])]

        self.stats = {stat["stat"]["name"]: stat["base_stat"] for stat in data.get("stats", [])}

        self.base_experience = data.get("base_experience")

        self.weight = str(int(data.get("weight"))*0.1)+" kg" if data.get("weight") > 1 else str(int(data.get("weight"))*100)+" g"
        self.height = str(int(data.get("height"))*10)+" cm"

        self.sprites = data.get("sprites", {})

    def __repr__(self):
        return (
            f"Pokemon(id={self.id}, name='{self.name}', types={self.types}, "
            f"abilities={self.abilities}, stats={self.stats}, "
            f"base_experience={self.base_experience}, "
            f"weight={self.weight}, height={self.height})"
        )