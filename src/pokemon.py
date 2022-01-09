import json
import math
from types import SimpleNamespace

from Ex4.client_python import client
from Ex4.client_python.client import Client
from Ex4.graph.DiGraph import DiGraph


class pokemon:

    def __init__(self, value, type, pos,graph: DiGraph):
        self.value = value
        self.type = type
        self.pos = pos
        final_src = None
        final_dest = None
        for src in graph.vertex.keys():
            srcNode = graph.vertex[src]
            for dest in graph.all_out_edges_of_node_help(src)[0].items():
                dest_num = dest[1][1]
                destNode = graph.vertex[dest_num]
                if (type > 0 and src < dest_num) or (type < 0 and src > dest_num):
                    positions = pos.split(',')
                    srcOne = [float(srcNode[0]), float(srcNode[1])]
                    destTwo = [float(destNode[0]), float(destNode[1])]
                    lineOne = math.dist(srcOne, destTwo)
                    lineTwo = math.dist(srcOne, [float(positions[0]),float(positions[1])]) + math.dist([float(positions[0]),float(positions[1])], destTwo)
                    if lineTwo - 0.0000001 <= lineOne <= lineTwo + 0.0000001:
                        final_src = src
                        final_dest = dest_num
                        break
            if final_src is not None:
                break
        self.src = final_src
        self.dest = final_dest

    def add_pokemon(self,id:int, pos:(),value:float, type:int):
        d = {self.num: (pos,value,type)}
        self.num += 1
        self.pokemons.update(d)

    def get_pokemon(self, id: int):
        return self.pokemons[id]

    def get_info(self):
        return Client.get_info()

    def get_src(self):
        return self.src

    def get_dest(self):
        return self.dest

    def distance(self, src, dest):
        src = [float(src[0]),float(src[1])]
        dest = [float(dest[0]),float(dest[1])]
        return math.dist(src, dest)
