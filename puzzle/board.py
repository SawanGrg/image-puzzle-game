#Hit137 Software Now
#Assessment3 - Image Puzzle Game
#Riwaj Shrestha (403312)
#Sawan Gurung (407504)
#Jung-Chuan Chiang (406089)

import random
import cv2
import numpy as np

from puzzle.tile import Tile
from transformations.swap import SwapTransformation
from transformations.rotate import RotateTransformation
from transformations.flip import FlipTransformation


class Board:

    def __init__(self, grid_size: int):
        self.grid_size = grid_size
        self.tiles = []
        self.original_image = None
        self.tile_width = 0
        self.tile_height = 0
        self.transformation_history = []

    @staticmethod
    def read_image(path: str):
        """Read an image file (JPG/PNG/BMP) and return it, or raise ValueError.

        cv2.imread cannot open paths with non-ASCII characters on Windows,
        so we read the bytes with numpy and decode them.
        """
        try:
            data = np.fromfile(path, dtype=np.uint8)
        except OSError as error:
            raise ValueError(f"Could not open {path}: {error}") from error

        image = cv2.imdecode(data, cv2.IMREAD_COLOR) if data.size else None
        if image is None:
            raise ValueError(f"Could not read image at {path}")
        return image

    def load_image(self, path: str, target_size: int = 360):
        image = self.read_image(path)
        image = self._resize_and_crop(image, target_size)
        self.original_image = image
        self._slice_into_tiles(image)

    def _resize_and_crop(self, image, target_size: int):
        """Centre-crop to a square, then resize so it divides evenly into the grid."""
        h, w = image.shape[:2]
        side = min(h, w)
        y0, x0 = (h - side) // 2, (w - side) // 2
        square = image[y0 : y0 + side, x0 : x0 + side]

        tile_dim = target_size // self.grid_size
        final_dim = tile_dim * self.grid_size
        interpolation = cv2.INTER_AREA if side > final_dim else cv2.INTER_CUBIC
        return cv2.resize(square, (final_dim, final_dim), interpolation=interpolation)

    def _slice_into_tiles(self, image):
        h, w = image.shape[:2]
        self.tile_height = h // self.grid_size
        self.tile_width = w // self.grid_size

        self.tiles = []
        tile_id = 0
        for row in range(self.grid_size):
            for col in range(self.grid_size):
                y0 = row * self.tile_height
                x0 = col * self.tile_width
                piece = image[
                    y0 : y0 + self.tile_height, x0 : x0 + self.tile_width
                ]
                position = row * self.grid_size + col
                self.tiles.append(Tile(piece, position, tile_id))
                tile_id += 1

    def scramble(self):
        total_moves = {3: 6, 4: 12, 5: 20}[self.grid_size]
        total_tiles = self.grid_size * self.grid_size

        max_swaps = min(total_tiles - total_moves, total_moves - 2)
        num_swaps = random.randint(1, max(1, max_swaps))

        remaining = total_moves - num_swaps
        num_rotates = random.randint(1, remaining - 1)
        num_flips = remaining - num_rotates

        swaps = [SwapTransformation() for _ in range(num_swaps)]
        singles = [RotateTransformation() for _ in range(num_rotates)] + [
            FlipTransformation() for _ in range(num_flips)
        ]
        random.shuffle(singles)
        plan = swaps + singles

        untouched = list(self.tiles)
        self.transformation_history = []

        for trans in plan:
            result = trans.apply(untouched)
            touched = result if isinstance(result, tuple) else (result,)
            for tile in touched:
                untouched.remove(tile)
            self.transformation_history.append(trans)

    def reassemble(self):
        canvas = self.original_image.copy()
        by_position = sorted(self.tiles, key=lambda t: t.current_position)

        for tile in by_position:
            row = tile.current_position // self.grid_size
            col = tile.current_position % self.grid_size
            y0 = row * self.tile_height
            x0 = col * self.tile_width
            canvas[y0 : y0 + self.tile_height, x0 : x0 + self.tile_width] = (
                tile.get_display_image()
            )

        return canvas

    def get_tile_at(self, x: int, y: int):
        if self.tile_width <= 0 or self.tile_height <= 0:
            return None
        if x < 0 or y < 0:
            return None
        col = x // self.tile_width
        row = y // self.tile_height

        if row >= self.grid_size or col >= self.grid_size:
            return None
        position = row * self.grid_size + col
        for tile in self.tiles:
            if tile.current_position == position:
                return tile
        return None

    def swap(self, tile_a, tile_b):
        tile_a.current_position, tile_b.current_position = (
            tile_b.current_position,
            tile_a.current_position,
        )

    def is_solved(self) -> bool:
        return all(tile.is_correct() for tile in self.tiles)

    def incorrect_count(self) -> int:
        return sum(1 for tile in self.tiles if not tile.is_correct())

    def solve(self):
        for trans in reversed(self.transformation_history):
            trans.undo()
        self.transformation_history.clear()

        for tile in self.tiles:
            tile.reset()
