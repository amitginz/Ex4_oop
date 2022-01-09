import json
import unittest

from Agent import agent
from Ex4.graph.DiGraph import DiGraph
from Ex4.graph.GraphAlgo import GraphAlgo
from pokemon import pokemon


class gatest(unittest.TestCase):

    def test_get_graph(self):
        g = DiGraph()
        g_algo = GraphAlgo(g)
        self.assertEqual(g_algo.get_graph(),g)

    def test_load_from_json(self):
        g_algo = GraphAlgo()  # init an empty graph - for the GraphAlgo
        file = "\\data\\T0.json"
        g_algo.load_from_json(file)  # init a GraphAlgo from a json file
        t = g_algo.get_graph()
        self.assertEqual(g_algo.get_graph(),t)

    def test_save_to_json(self):
        g_algo = GraphAlgo()  # init an empty graph - for the GraphAlgo
        file = "\\data\\T0.json"
        g_algo.load_from_json(file)  # init a GraphAlgo from a json file
        t = g_algo.get_graph()
        g_algo.save_to_json(file + '_saved')
        self.assertEqual(g_algo.get_graph(),t)

    def test_shortest_path(self):
        g_algo = GraphAlgo()
        file = '\\data\\A5.json'
        g_algo.load_from_json(file)
        g_algo.get_graph().remove_edge(13, 14)
        g_algo.save_to_json(file + "_edited")
        dist,path = g_algo.shortest_path(1, 7)
        self.assertEqual(g_algo.shortest_path(1,7),(dist,path))
        dist,path = g_algo.shortest_path(47, 19)
        self.assertEqual(g_algo.shortest_path(47,19),(dist,path))
        dist, path = g_algo.shortest_path(20, 2)
        self.assertEqual(g_algo.shortest_path(20,2),(dist,path))
        dist, path= g_algo.shortest_path(2, 20)
        self.assertEqual(g_algo.shortest_path(2,20),(dist,path))

    def test_TSP(self):
        g_algo = GraphAlgo()
        file = '\\data\\A5.json'
        g_algo.load_from_json(file)
        self.assertEqual(g_algo.TSP([1, 2, 3]),([1, 9, 2, 3], 5.334107079683037))
        g_algo.TSP([2, 5, 3])
        self.assertEqual(g_algo.TSP([2, 5, 3]),([2, 3, 13, 5], 6.5323832186875235))

    def test_isconnected(self):
        g_algo = GraphAlgo()  # init an empty graph - for the GraphAlgo
        file = "\\data\\A0.json"
        g_algo.load_from_json(file)  # init a GraphAlgo from a json file
        t = g_algo.get_graph()
        self.assertEqual(g_algo.is_connected(),True)

    def test_centerPoint(self):
        g_algo = GraphAlgo()  # init an empty graph - for the GraphAlgo
        file = "\\data\\A0.json"
        g_algo.load_from_json(file)  # init a GraphAlgo from a json file
        t = g_algo.get_graph()
        self.assertEqual(g_algo.centerPoint(),(7, 6.806805834715163))

    def test_dijkstra(self):
        g_algo = GraphAlgo()  # init an empty graph - for the GraphAlgo
        file = "\\data\\A0.json"
        g_algo.load_from_json(file)  # init a GraphAlgo from a json file
        tes,res = g_algo.dijkstra(0)
        self.assertEqual(g_algo.dijkstra(0),(tes,res))
        file = "\\data\\A5.json"
        g_algo.load_from_json(file)  # init a GraphAlgo from a json file
        tes,res = g_algo.dijkstra(0)
        self.assertEqual(g_algo.dijkstra(0),(tes,res))
        file = "\\data\\A3.json"
        g_algo.load_from_json(file)  # init a GraphAlgo from a json file
        tes,res = g_algo.dijkstra(0)
        self.assertEqual(g_algo.dijkstra(0),(tes,res))

    def test_get_Agents(self):
        g_algo = GraphAlgo()
        age = {
            "Agents":[
                {
                    "Agent":
                    {
                        "id":0,
                        "value":0.0,
                        "src":0,
                        "dest":1,
                        "speed":1.0,
                        "pos":"35.18753053591606,32.10378225882353,0.0"
                    }
                }
            ]
        }
        json_object = json.dumps(age, indent = 4)
        agent_tmp = g_algo.getAgent(json_object)
        age1 = agent(0,0,0,1,1,(35.18753053591606,32.10378225882353))
        self.assertEqual(agent_tmp,age1)


    def test_get_pokemons(self):
        g_algo = GraphAlgo()
        poke = {
            "Pokemons":[
                {
                    "Pokemon":{
                        "value":5.0,
                        "type":-1,
                        "pos":"35.197656770719604,32.10191878639921,0.0"
                    }
                }
            ]
        }
        json_object = json.dumps(poke, indent = 4)
        poke_tmp = g_algo.getPokemons(json_object)
        poke1 = pokemon(5,-1,(35.197656770719604,32.10191878639921),g_algo.get_graph())
        self.assertEqual(poke1,poke_tmp)


    def test_choosePokForAgent(self):
        pass
