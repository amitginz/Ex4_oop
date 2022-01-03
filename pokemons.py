

class pokemons:

    def __init__(self, pokemons: dict = {}):
        self.pokemons: dict = pokemons
        self.num = 0

    def add_pokemon(self,id:int, pos:(),value:float, type:int):
        d = {self.num: (pos,value,type)}
        self.num += 1
        self.pokemons.update(d)

    def get_pokemon(self, id: int):
        return self.pokemons[id]

    def get_info(self):
        return self.pokemons.__repr__()
