import json
import math
import os
import sys
from typing import List

import pygame
from matplotlib import pyplot as plt
from pygame import display, RESIZABLE, gfxdraw

from DiGraph import DiGraph
import GraphInterface
from GraphAlgoInterface import GraphAlgoInterface

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
        with open(root_path + file_name, 'r') as file:
            g = json.load(file)
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

    #draw the graph in the screen
    def plot_graph(self) -> None:
        radius = 15

        while (True):
            # check events
            for event in pygame.event.get():
                if event.type == pygame.QUIT:
                    pygame.quit()
                    exit(0)

            # refresh screen
            screen.fill(pygame.Color(0, 0, 0))

            # draw nodes
            for n in self.graph.vertex:
                x = self.my_scale(self.graph.vertex[n][0], x=True)
                y = self.my_scale(self.graph.vertex[n][1], y=True)

                # its just to get a nice antialiased circle
                gfxdraw.filled_circle(screen, int(x), int(y), radius, pygame.Color(64, 80, 174))
                gfxdraw.aacircle(screen, int(x), int(y), radius, pygame.Color(255, 255, 255))

                # draw the node id
                id_srf = FONT.render(str(n), True, pygame.Color(255, 255, 255))
                rect = id_srf.get_rect(center=(x, y))
                screen.blit(id_srf, rect)

            # draw edges
            for e in self.graph.edges:
                # find the edge nodes
                src = next(n for n in self.graph.vertex if n == e[0])
                dest = next(n for n in self.graph.vertex if n == e[1])

                # scaled positions
                src_x = self.my_scale(self.graph.vertex[src][0], x=True)
                src_y = self.my_scale(self.graph.vertex[src][1], y=True)
                dest_x = self.my_scale(self.graph.vertex[dest][0], x=True)
                dest_y = self.my_scale(self.graph.vertex[dest][1], y=True)

                # draw the line
                pygame.draw.line(screen, pygame.Color(61, 72, 126), (src_x, src_y), (dest_x, dest_y))
                ang = self.GetAngleOfLineBetweenTwoPoints((dest_x,dest_y),(src_x,src_y))
                self.DrawArrow(dest_x, dest_y, pygame.Color(0, 255, 255), ang)
            # update screen changes
            display.update()

            # refresh rate
            clock.tick(60)


    #get the angle of some arrow
    def GetAngleOfLineBetweenTwoPoints(self,p1, p2):
        xDiff = p2[0] - p1[0]
        yDiff = p2[1] - p1[1]
        return math.degrees(math.atan2(yDiff, xDiff))

    #draw the arrow
    def DrawArrow(self, x, y, color, angle=0):
        def rotate(pos, angle):
            cen = (5 + x, 0 + y)
            angle *= -(math.pi / 180)
            cos_theta = math.cos(angle)
            sin_theta = math.sin(angle)
            ret = ((cos_theta * (pos[0] - cen[0]) - sin_theta * (pos[1] - cen[1])) + cen[0],
                   (sin_theta * (pos[0] - cen[0]) + cos_theta * (pos[1] - cen[1])) + cen[1])
            return ret

        p0 = rotate((0 + x, -4 + y), angle + 90)
        p1 = rotate((0 + x, 4 + y), angle + 90)
        p2 = rotate((10 + x, 0 + y), angle + 90)

        pygame.draw.polygon(screen, color, [p0, p1, p2])

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

    # scale the point[X] to be seen in the graph
    def scaleX(self, data, min_screen, max_screen, min_data, max_data):
        """
        get the scaled data with proportions min_data, max_data
        relative to min and max screen dimensions
        """
        abs1 = abs(max_data - min_data);
        scaleX = screen.get_width() / abs1;
        return ((data) * (max_screen - min_screen) * scaleX) % screen.get_width() + min_screen

    # scale the point[Y] to be seen in the graph
    def scaleY(self, data, min_screen, max_screen, min_data, max_data):
        """
        get the scaled data with proportions min_data, max_data
        relative to min and max screen dimensions
        """
        abs1 = abs(max_data - min_data);
        scaleY = screen.get_height() / abs1;
        return ((data) * (max_screen - min_screen) * scaleY) % screen.get_height() + min_screen

    # scale the point to be seen in the graph
    def my_scale(self, data, x=False, y=False):
        # get data proportions
        min_x = 0
        min_y = 0
        max_x = 0
        max_y = 0
        for i in range(0, len(self.graph.vertex) - 1):
            x = self.graph.vertex[i][0]
            min_x = min(self.graph.vertex[i + 1][0], x)
        for i in range(0, len(self.graph.vertex) - 1):
            y = self.graph.vertex[i][1]
            min_y = min(self.graph.vertex[i + 1][1], y)
        for i in range(0, len(self.graph.vertex) - 1):
            x1 = self.graph.vertex[i][0]
            max_x = max(self.graph.vertex[i + 1][0], x1)
        for i in range(0, len(self.graph.vertex) - 1):
            y1 = self.graph.vertex[i][1]
            max_y = max(self.graph.vertex[i + 1][1], y1)
        if x:
            return self.scaleY(data, 10, screen.get_width() - 55, min_y, max_y)
        if y:
            return self.scaleX(data, 40, screen.get_height() - 40, min_x, max_x)
