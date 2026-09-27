import random

from .base import Transformation


class FlipTransformation(Transformation):
    def __init__(self):
        super().__init__("flip")

    def apply(self, tiles):
        tile = random.choice(tiles)
        horizontal = random.choice([True, False])
        tile.apply_flip(
            horizontal=horizontal,
            vertical=not horizontal
        )
        return tile