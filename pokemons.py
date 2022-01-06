import json
from types import SimpleNamespace

from Ex4.client_python import client
from Ex4.client_python.client import Client


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
        return Client.get_info()

    def load_pokemon(self):
        pokemons = client.get_pokemons()
        pokemons_obj = json.loads(pokemons, object_hook=lambda d: SimpleNamespace(**d))
        return pokemons_obj
