#Hit137 Software Now
#Assessment3 - Image Puzzle Game
#Riwaj Shrestha (403312)
#Sawan Gurung (407504)
#Jung-Chuan Chiang (406089)

import random
from .base import Transformation


class SwapTransformation(Transformation):

    def __init__(self):
        super().__init__("swap")
        self._tile_a = None
        self._tile_b = None

    def apply(self, tiles: list):
        self._tile_a, self._tile_b = random.sample(tiles, 2)
        self._exchange_positions()
        return self._tile_a, self._tile_b

    def undo(self):
        if self._tile_a and self._tile_b:
            self._exchange_positions()

    def _exchange_positions(self):
        self._tile_a.current_position, self._tile_b.current_position = (
            self._tile_b.current_position,
            self._tile_a.current_position,
        )