#Hit137 Software Now
#Assessment3 - Image Puzzle Game
#Riwaj Shrestha (403312)
#Sawan Gurung (407504)
#Jung-Chuan Chiang (406089)

import random
from .base import Transformation


class RotateTransformation(Transformation):

    def __init__(self):
        super().__init__("rotate")
        self._tile = None
        self._degrees = 0

    def apply(self, tiles: list):
        self._tile = random.choice(tiles)
        self._degrees = random.choice([90, 180, 270])
        self._tile.apply_rotation(self._degrees)
        return self._tile

    def undo(self):
        if self._tile and self._degrees != 0:
            self._tile.apply_rotation(-self._degrees)