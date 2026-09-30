import random
from .base import Transformation


class FlipTransformation(Transformation):

    def __init__(self):
        super().__init__("flip")
        self.tile = None
        self.is_vertical = False

    def apply(self, tiles: list):
        self.tile = random.choice(tiles)
        self.is_vertical = random.choice([True, False])

        if self.is_vertical:
            self.tile.apply_flip(vertical=True)
        else:
            self.tile.apply_flip(horizontal=True)

        return self.tile

    def undo(self):
        if self.tile:
            if self.is_vertical:
                self.tile.apply_flip(vertical=True)
            else:
                self.tile.apply_flip(horizontal=True)
