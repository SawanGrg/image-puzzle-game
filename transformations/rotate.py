import random

from .base import Transformation


class RotateTransformation(Transformation):
    def __init__(self):
        super().__init__("rotate")

    def apply(self, tiles):
        tile = random.choice(tiles)
        degrees = random.choice([90, 180, 270])
        tile.apply_rotation(degrees)
        return tile