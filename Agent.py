from math import sqrt

from Ex4.client_dierctory.DiGraph import DiGraph
from GraphAlgo import GraphAlgo
from pokemons import pokemons


class agent:
    def __init__(self, agents: dict = {}, location: dict = {}):
        self.agents: dict = agents
        self.location: dict = location
        self.count_move = 0

    def move(self, pos: (0, 0), id: int) -> None:
        self.location[id] = pos
        self.count_move += 1

    def add_agent(self, id: int, pos: (0, 0)) -> None:
        d = {id: pos}
        self.agents.update(d)

    def remove_agent(self, id: int) -> None:
        del self.agents[id]
        del self.location[id]

    def get_agent(self, id: int) -> dict:
        return self.agents[id]

    def chooseNextEdge(self, id: int) -> dict:
        path = GraphAlgo.dijkstra(self.location[id])[1]
        di = {"agent_id": id, "next_node_id": path[self.pokemon_edge(id)]}
        return di

    def pokemon_edge(self, id: int) -> dict:  # locate the edge the pokemon on it
        graph = DiGraph();
        poke = pokemons()
        for i,j in graph:
            if graph.edges[(i,j)] is not None:
                if self.is_between(i,poke[id],j):
                    return (i,j)

    def distance(self,a,b):
        return sqrt((a.x - b.x)**2 + (a.y - b.y)**2)

    def is_between(self,a,c,b):
        return self.distance(a,c) + self.distance(c,b) == self.distance(a,b)

    # def get_graph(self):
    #     graph_algo = GraphAlgo()
    #     graph_algo.load_from_json("data\\A0.json")
    #     return graph_algo.get_graph()

