#Hit137 Software Now
#Assessment3 - Image Puzzle Game
#Riwaj Shrestha (403312)
#Sawan Gurung (407504)
#Jung-Chuan Chiang (406089)

import random
from .base import Transformation


class FlipTransformation(Transformation):

    def __init__(self):
        super().__init__("flip")
        self._tile = None
        self._is_vertical = False

    def apply(self, tiles: list):
        self._tile = random.choice(tiles)
        self._is_vertical = random.choice([True, False])
        self._flip()
        return self._tile

    def undo(self):
        if self._tile:
            self._flip()  

    def _flip(self):
        if self._is_vertical:
            self._tile.apply_flip(vertical=True)
        else:
            self._tile.apply_flip(horizontal=True)