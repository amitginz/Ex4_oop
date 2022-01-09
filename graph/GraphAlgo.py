import json
import math
import os
from typing import List

import pygame
from pygame import display, RESIZABLE, gfxdraw

import Agent
from Agent import agent
from DiGraph import DiGraph
import GraphInterface
from GraphAlgoInterface import GraphAlgoInterface
from pokemon import pokemon

INF = 99999999
root_path = os.path.dirname(os.path.abspath(__file__))
#init pygame
WIDTH, HEIGHT = 1000, 800

pygame.init()
screen = display.set_mode((WIDTH, HEIGHT), depth=32, flags=RESIZABLE)
clock = pygame.time.Clock()
pygame.font.init()

FONT = pygame.font.SysFont('Arial', 20, bold=True)


class GraphAlgo(GraphAlgoInterface):

    # a constructor for algograph
    def __init__(self, graph: DiGraph = {}):
        self.graph: dict = graph

    # get the graph of graphalgo
    def get_graph(self) -> GraphInterface:
        return self.graph

    # load the graph from json file
    def load_from_json(self, file_name: str) -> bool:
        with open(file_name, 'r') as file:
            g = json.load(file_name)
        if g is None:
            return False
        graph = DiGraph()
        for n in g["Nodes"]:
            if 'pos' not in n:
                graph.add_node(node_id=n["id"], pos=(0, 0))
            else:
                sp = str(n['pos']).split(',')
                graph.add_node(node_id=int(n["id"]), pos=(float(sp[0]), float(sp[1])))
        for v in g["Edges"]:
            graph.add_edge(id1=v['src'], id2=v['dest'], weight=v['w'])
        self.__init__(graph)
        return True

    # save the graph to json file
    def save_to_json(self, file_name: str) -> bool:
        list = []
        dict = {'Nodes': {(i): self.graph.vertex[i] for i in self.graph.vertex}}
        list.append(dict)
        dict1 = {'Edges': ''}
        list.append(dict1)
        for i in self.graph.vertex:
            for j in self.graph.all_out_edges_of_node(i)[0]:
                edge = {'src': i, 'dest': j, 'weight': self.graph.edges[(i, j)]}
                list.append(edge)
        out_file = open(root_path + file_name, "w")
        json.dump(list, out_file, indent=2)
        out_file.close()
        if out_file is None:
            return False
        return True

    # calculate the distance between two points in the graph
    def shortest_path(self, id1: int, id2: int) -> (float, list):
        shortest = []
        dist, path = self.dijkstra(id1)
        if id1 == -1 or id2 == -1:
            return float('inf'), []
        i = id2
        if dist[id2] != INF:
            shortest.append(id2)
            while i != id1:
                shortest.append(path[i])
                i = path[i]
            shortest.reverse()
        if dist[id2] == INF:
            dist[id2] = float('inf')
        return dist[id2], shortest

    # calculate TSP between point in list from the graph
    def TSP(self, node_lst: List[int]) -> (List[int], float):
        help = []
        ans = []
        sum = 0
        start = INF
        for i in range(0, len(node_lst)):
            help.append(node_lst[i])
        cur = node_lst[0]
        help.remove(help[0])
        while len(help) >= 1:
            for i in range(0, len(help)):
                key = help[i]
                if self.shortest_path_help(cur, key) < start:
                    shortestdist, lst = self.shortest_path(cur, key)
                    sum += shortestdist
            ans.append(lst)
            cur = help[i]
            help.pop(i);
        answer = []
        for i in ans:
            for j in i:
                if j not in answer:
                    answer.append(j)
        return answer, sum

    # check if the graph isconneceted or not
    def is_connected(self):
        return INF not in self.dijkstra(0)[0]

    # calc the center of sum graph
    def centerPoint(self) -> (int, float):
        if not self.is_connected():
            return None, None
        list = []
        for i in self.graph.vertex:
            dist = self.dijkstra(i)[0]  # list of distances
            # find maximum
            max = 0
            for j in range(len(dist)):
                if dist[j] > max:
                    max = dist[j]
            list.insert(i, max)
            max = 0
        min = float('inf')

        for i in range(len(list)):
            if min > list[i]:
                min = list[i]
                node = i

        return node, min

    # a function to calculate the shortestpath dist
    def shortest_path_help(self, id1: int, id2: int) -> (float):
        dist, path = self.dijkstra(id1)
        if id1 == -1 or id2 == -1:
            return float('inf')
        return dist[id2]


    # a function of the algorithm of dijkstra
    def dijkstra(self, start_node):
        unvisited_nodes = list(self.graph.vertex)
        # We'll use this dict to save the cost of visiting each node and update it as we move along the graph
        dist = {}
        # We'll use this dict to save the shortest known path to a node found so far
        path = {}
        # We'll use max_value to initialize the "infinity" value of the unvisited nodes
        for node in unvisited_nodes:
            dist[node] = INF
            # However, we initialize the starting node's value with 0
            dist[start_node] = 0

        # The algorithm executes until we visit all nodes
        while unvisited_nodes:
            # The code block below finds the node with the lowest score
            current_min_node = None
            for node in unvisited_nodes:  # Iterate over the nodes
                if current_min_node == None:
                    current_min_node = node
                elif dist[node] < dist[current_min_node]:
                    current_min_node = node

            # The code block below retrieves the current node's neighbors and updates their distances
            neighbors = self.graph.all_out_edges_of_node(current_min_node)[0]
            for neighbor in neighbors:
                tentative_value = dist[current_min_node] + self.graph.edges[(current_min_node, neighbor)]
                if tentative_value < dist[neighbor]:
                    dist[neighbor] = tentative_value
                    # We also update the best path to the current node
                    path[neighbor] = current_min_node
            # After visiting its neighbors, we mark the node as "visited"
            unvisited_nodes.remove(current_min_node)
        return dist, path


    def choosePokForAgent(self, agent: Agent,pokemons:dict):
        minDist = float('inf')
        pokemonMin = None
        index=None
        next_node=None
        for p, pokemon in pokemons.items():
            if agent.src == pokemon.src:
                return pokemon, pokemon.get_dest()
            dist, next_node_temp = self.shortest_path(agent.get_src(), pokemon.get_src())
            if dist < minDist:
                minDist = dist
                pokemonMin = pokemon
                index = p
                if len(next_node_temp)==1:
                    next_node=next_node_temp[0]
                else:
                    next_node = next_node_temp[1]
        del pokemons[index]
        return pokemonMin, next_node

    def getAgents(self, file: str) -> dict:
        agents = {}
        dict = json.loads(file)
        for n in range(len(dict["Agents"])):
            id = dict["Agents"][n]["Agent"]["id"]
            value = dict["Agents"][n]["Agent"]["value"]
            src = dict["Agents"][n]["Agent"]["src"]
            dest = dict["Agents"][n]["Agent"]["dest"]
            speed = dict["Agents"][n]["Agent"]["speed"]
            pos = dict["Agents"][n]["Agent"]["pos"]
            agent1 = agent(id, value, src, dest, speed, pos)
            agents[n] = agent1
        return agents

    def getPokemons(self, string: str) -> dict:
        pokemons = {}
        dict = json.loads(string)
        for n in range(len(dict["Pokemons"])):
            value = dict["Pokemons"][n]["Pokemon"]["value"]
            type = dict["Pokemons"][n]["Pokemon"]["type"]
            pos = dict["Pokemons"][n]["Pokemon"]["pos"]
            p = pokemon(value, type, pos,self.graph)
            pokemons[n] = p
        return pokemons
