import json
from types import SimpleNamespace

from Ex4.client_python import client
from Ex4.client_python.client import Client


class pokemon:

    def __init__(self, value, type, pos):
        self.value = value
        self.type = type
        self.pos = pos

    def add_pokemon(self,id:int, pos:(),value:float, type:int):
        d = {self.num: (pos,value,type)}
        self.num += 1
        self.pokemons.update(d)

    def get_pokemon(self, id: int):
        return self.pokemons[id]

    def get_info(self):
        return Client.get_info()

    def load_pokemon(self,string):
        pokemons = []
        dict1 = json.loads(string)
        for n in dict1["Pokemons"]:
            value = n["Pokemon"]["value"]
            type = n["Pokemon"]["type"]
            pos = n["Pokemon"]["pos"]
            p = pokemon(value, type, pos)
            pokemons.append(p)
        return pokemons
