import random
from .base import Transformation


class RotateTransformation(Transformation):
    """Rotates one random tile by 90, 180 or 270 degrees."""

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