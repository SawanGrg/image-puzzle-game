import random
from .base import Transformation


class SwapTransformation(Transformation):

    def __init__(self):
        super().__init__("swap")
        self.tile_a = None
        self.tile_b = None

    def apply(self, tiles: list):
        self.tile_a, self.tile_b = random.sample(tiles, 2)

        self.tile_a.current_position, self.tile_b.current_position = (
            self.tile_b.current_position,
            self.tile_a.current_position,
        )

        return self.tile_a, self.tile_b

    def undo(self):
        if self.tile_a and self.tile_b:
            self.tile_a.current_position, self.tile_b.current_position = (
                self.tile_b.current_position,
                self.tile_a.current_position,
            )
