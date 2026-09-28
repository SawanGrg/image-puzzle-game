import random
from .base import Transformation


class RotateTransformation(Transformation):

    def __init__(self):
        super().__init__("rotate")
        self.tile = None
        self.degrees = 0

    def apply(self, tiles: list):
        self.tile = random.choice(tiles)
        self.degrees = random.choice([90, 180, 270])
        self.tile.apply_rotation(self.degrees)
        return self.tile

    def undo(self):
        if self.tile and self.degrees != 0:
            self.tile.apply_rotation(-self.degrees)
