import json
from math import sqrt
from types import SimpleNamespace
import algo_game
import pokemon


class agent1:

    def __init__(self, id, value, src, dest, speed, pos):
        self.id = id
        self.value = value
        self.src = src
        self.dest = dest
        self.speed = speed
        self.pos = pos

    def __repr__(self) -> str:
        return "{{'Agent': id:{} value:{} src:{} dest:{} speed:{} pos:{}}}" \
            .format(self.id, self.value, self.src, self.dest, self.speed, self.pos)

    def get_id(self):
        return self.id

    def get_value(self):
        return self.value

    def get_src(self):
        return self.src

    def get_dest(self):
        return self.dest

    def get_speed(self):
        return self.speed

    def get_pos(self):
        return self.pos
