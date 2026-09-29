import random
from .base import Transformation


class FlipTransformation(Transformation):

    def __init__(self):
        super().__init__("flip")
        self.tile = None
        self.rotated_180 = False

    def apply(self, tiles: list):
        self.tile = random.choice(tiles)

        is_vertical = random.choice([True, False])
        if is_vertical:
            self.tile.apply_flip(horizontal=True)
            self.tile.apply_rotation(180)
            self.rotated_180 = True
        else:
            self.tile.apply_flip(horizontal=True)
            self.rotated_180 = False

        return self.tile

    def undo(self):
        if self.tile:
            if self.rotated_180:
                self.tile.apply_rotation(-180)
            self.tile.apply_flip(horizontal=True)
