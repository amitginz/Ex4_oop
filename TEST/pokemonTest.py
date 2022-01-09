import unittest

from pokemon import pokemon


class poke_test(unittest.TestCase):
    def test_get_pokemon(self):
        po = pokemon(6, -1, (0, 1), None)
        self.assertEqual(po.get_pokemon(0), (6, -1, (0, 1), None))


    def test_add_pokemon(self):
        po = pokemon(6, -1, (0, 1), None)
        self.assertEqual(po.add_pokemon(6, -1, (0, 1)) , {po})

    def test_get_src(self):
        po = pokemon(6, -1, (0, 1), None)
        self.assertEqual(po.get_src(), None)
        pass

    def test_get_dest(self):
        po = pokemon(6, -1, (0, 1), None)
        self.assertEqual(po.get_dest(), None)
