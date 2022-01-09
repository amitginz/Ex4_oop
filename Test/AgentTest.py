import unittest

from Agent import agent


class agenttest(unittest.TestCase):

    def test_get_id(self):
        age = agent(0, 5, 0,2,6, (35,32))
        self.assertEqual(age.get_id(),0)

    def test_get_value(self):
        age = agent(0, 5, 0,2,6, (35,32))
        self.assertEqual(age.get_value(),5)

    def test_get_src(self):
        age = agent(0, 5, 0,2,6, (35,32))
        self.assertEqual(age.get_src(),0)

    def test_get_dest(self):
        age = agent(0, 5, 0,2,6, (35,32))
        self.assertEqual(age.get_dest(),2)

    def test_get_speed(self):
        age = agent(0, 5, 0,2,6, (35,32))
        self.assertEqual(age.get_speed(),6)

    def test_get_pos(self):
        age = agent(0, 5, 0,2,6, (35,32))
        self.assertEqual(age.get_pos(),(35,32))

    def test_repr(self):
        age = agent(0, 5, 0,2,6, (35,32))
        str = "{'Agent': id:0 value:5 src:0 dest:2 speed:6 pos:(35, 32)}"
        self.assertEqual(age.__repr__(),str)

