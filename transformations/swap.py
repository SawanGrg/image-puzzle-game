import random

from .base import Transformation


class SwapTransformation(Transformation):
    def __init__(self):
        super().__init__("swap")

    def apply(self, tiles):
        tile_a, tile_b = random.sample(tiles, 2)

        tile_a.current_position, tile_b.current_position = (
            tile_b.current_position,
            tile_a.current_position
        )

        return tile_a, tile_b