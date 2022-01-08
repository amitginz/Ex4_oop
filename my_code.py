# init pygame
from operator import mod
from types import SimpleNamespace

import pygame
from pygame import display
import json
from pygame import gfxdraw
import pygame
from pygame import *

from Ex4.client_python.client import Client
from Ex4.graph.DiGraph import DiGraph
from Ex4.graph.GraphAlgo import GraphAlgo
from algo_game import algo_game
from pokemon import pokemon

WIDTH, HEIGHT = 1080, 720

# default port
PORT = 6666
# server host (default localhost 127.0.0.1)
HOST = '127.0.0.1'
pygame.init()

screen = display.set_mode((WIDTH, HEIGHT), depth=32, flags=RESIZABLE)
clock = pygame.time.Clock()
pygame.font.init()

client = Client()
client.start_connection(HOST, PORT)

pokemons = client.get_pokemons()
poke = pokemon(0,0,0)
poke.load_pokemon(pokemons)

graph_json = client.get_graph()

FONT = pygame.font.SysFont('Arial', 20, bold=True)


data = json.loads(graph_json)
Edges = data["Edges"]
Nodes = data["Nodes"]
dgi = DiGraph({}, {})
for n in Nodes:
    sp = n['pos'].split(',')
    id1 = n['id']
    dgi.add_node(id1,(float(sp[0]),float(sp[1])))
for e in Edges:
    src = e['src']
    dest = e['dest']
    weight = e['w']
    dgi.add_edge(int(src), int(dest),float(weight))


algo = GraphAlgo()
algo.__init__(dgi)



pokemons = client.get_pokemons()
pokemons_obj = json.loads(pokemons, object_hook=lambda d: SimpleNamespace(**d))

print(pokemons)

graph_json = client.get_graph()

FONT = pygame.font.SysFont('Arial', 20, bold=True)
# load the json string into SimpleNamespace Object

graph = json.loads(
    graph_json, object_hook=lambda json_dict: SimpleNamespace(**json_dict))



for n in graph.Nodes:
    x, y, _ = n.pos.split(',')
    n.pos = SimpleNamespace(x=float(x), y=float(y))

 # get data proportions
min_x = min(list(graph.Nodes), key=lambda n: n.pos.x).pos.x
min_y = min(list(graph.Nodes), key=lambda n: n.pos.y).pos.y
max_x = max(list(graph.Nodes), key=lambda n: n.pos.x).pos.x
max_y = max(list(graph.Nodes), key=lambda n: n.pos.y).pos.y


def scale(data, min_screen, max_screen, min_data, max_data):
    """
    get the scaled data with proportions min_data, max_data
    relative to min and max screen dimentions
    """
    return ((data - min_data) / (max_data-min_data)) * (max_screen - min_screen) + min_screen


# decorate scale with the correct values

def my_scale(data, x=False, y=False):
    if x:
        return scale(data, 50, screen.get_width() - 50, min_x, max_x)
    if y:
        return scale(data, 50, screen.get_height()-50, min_y, max_y)


radius = 15

client.add_agent("{\"id\":0}")
#client.add_agent("{\"id\":1}")
#client.add_agent("{\"id\":2}")
#client.add_agent("{\"id\":3}")

# this commnad starts the server - the game is running now
client.start()

"""
The code below should be improved significantly:
The GUI and the "algo" are mixed - refactoring using MVC design pattern is required.
"""
i = 1
while client.is_running() == 'true':
    pokemons = json.loads(client.get_pokemons(),
                          object_hook=lambda d: SimpleNamespace(**d)).Pokemons
    pokemons = [p.Pokemon for p in pokemons]
    for p in pokemons:
        x, y, _ = p.pos.split(',')
        p.pos = SimpleNamespace(x=my_scale(
            float(x), x=True), y=my_scale(float(y), y=True))
    agents = json.loads(client.get_agents(),
                        object_hook=lambda d: SimpleNamespace(**d)).Agents
    agents = [agent.Agent for agent in agents]
    for a in agents:
        x, y, _ = a.pos.split(',')
        a.pos = SimpleNamespace(x=my_scale(
            float(x), x=True), y=my_scale(float(y), y=True))
    # check events
    for event in pygame.event.get():
        if event.type == pygame.QUIT:
            pygame.quit()
            exit(0)

    # refresh surface
    screen.fill(Color(0, 0, 0))

    # draw nodes
    for n in graph.Nodes:
        x = my_scale(n.pos.x, x=True)
        y = my_scale(n.pos.y, y=True)

        # its just to get a nice antialiased circle
        gfxdraw.filled_circle(screen, int(x), int(y),
                              radius, Color(64, 80, 174))
        gfxdraw.aacircle(screen, int(x), int(y),
                         radius, Color(255, 255, 255))

        # draw the node id
        id_srf = FONT.render(str(n.id), True, Color(255, 255, 255))
        rect = id_srf.get_rect(center=(x, y))
        screen.blit(id_srf, rect)

    # draw edges
    for e in graph.Edges:
        # find the edge nodes
        src = next(n for n in graph.Nodes if n.id == e.src)
        dest = next(n for n in graph.Nodes if n.id == e.dest)

        # scaled positions
        src_x = my_scale(src.pos.x, x=True)
        src_y = my_scale(src.pos.y, y=True)
        dest_x = my_scale(dest.pos.x, x=True)
        dest_y = my_scale(dest.pos.y, y=True)

        # draw the line
        pygame.draw.line(screen, Color(61, 72, 126),
                         (src_x, src_y), (dest_x, dest_y))

    # draw agents
    for agent in agents:
        pygame.draw.circle(screen, Color(122, 61, 23),
                           (int(agent.pos.x), int(agent.pos.y)), 10)
    # draw pokemons (note: should differ (GUI wise) between the up and the down pokemons (currently they are marked in the same way).
    for p in pokemons:
        if p.type == -1:
            pygame.draw.circle(screen, Color(0, 255, 255), (int(p.pos.x), int(p.pos.y)), 10)
        else:
            pygame.draw.circle(screen, Color(255, 0, 255), (int(p.pos.x), int(p.pos.y)), 10)

    # update screen changes
    display.update()

    # refresh rate
    clock.tick(60)

    # choose next edge

    for agent in agents:
        if agent.dest == -1:
            path = algo.dijkstra(agent.src)[1]
            next_node = path[(len(graph.Nodes)-i)% len(graph.Nodes)]
            #next_node = (agent.src -1) % len(graph.Nodes)
            client.choose_next_edge(
                '{"agent_id":'+str(agent.id)+', "next_node_id":'+str(next_node)+'}')
            i += 1
        # if agent.dest == 1:
        #     path = algo.dijkstra(agent.src)[1]
        #     if path[i % len(graph.Nodes)] is not None:
        #         next_node = path[i % len(graph.Nodes)]
        #     #next_node = (agent.src -1) % len(graph.Nodes)
        #     client.choose_next_edge(
        #         '{"agent_id":'+str(agent.id)+', "next_node_id":'+str(next_node)+'}')
        #     i += 1
        ttl = client.time_to_end()
        print(ttl, client.get_info())
        # for p in pokemons:
        #     if agent.pos == p.pos:
        #         client.move()
    client.move()
# game over:
