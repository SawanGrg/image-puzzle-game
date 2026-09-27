import random

import cv2

from puzzle.tile import Tile
from transformations.swap import SwapTransformation
from transformations.rotate import RotateTransformation
from transformations.flip import FlipTransformation


class Board:
    def __init__(self, grid_size):
        self.grid_size = grid_size
        self.tiles = []
        self.original_image = None   # untouched, for the left canvas
        self.tile_width = 0
        self.tile_height = 0

    # ------------------------------------------------------------------
    # Loading and slicing
    # ------------------------------------------------------------------

    def load_image(self, path, target_width=600, target_height=600):
        image = cv2.imread(path)
        if image is None:
            raise ValueError(f"Could not read image at {path}")

        image = self._resize_to_fit(image, target_width, target_height)
        image = self._crop_to_grid(image)

        self.original_image = image
        self._slice_into_tiles(image)

    def _resize_to_fit(self, image, target_width, target_height):
        h, w = image.shape[:2]
        scale = min(target_width / w, target_height / h)
        new_w, new_h = int(w * scale), int(h * scale)
        return cv2.resize(image, (new_w, new_h))

    def _crop_to_grid(self, image):
        h, w = image.shape[:2]
        # crop down to the nearest multiple of grid_size in each dimension
        new_h = h - (h % self.grid_size)
        new_w = w - (w % self.grid_size)
        return image[0:new_h, 0:new_w]

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
                piece = image[y0:y0 + self.tile_height, x0:x0 + self.tile_width]
                position = row * self.grid_size + col
                self.tiles.append(Tile(piece, position, tile_id))
                tile_id += 1

    # ------------------------------------------------------------------
    # Scrambling
    # ------------------------------------------------------------------

    def scramble(self):
        transformation_count = {3: 6, 4: 12, 5: 20}[self.grid_size]
        transformation_types = [SwapTransformation, RotateTransformation, FlipTransformation]

        untouched = list(self.tiles)
        applied = 0

        while applied < transformation_count and len(untouched) >= 1:
            transformation_cls = random.choice(transformation_types)
            transformation = transformation_cls()

            # SwapTransformation needs 2 untouched tiles; skip it if only 1 remains
            if isinstance(transformation, SwapTransformation) and len(untouched) < 2:
                continue

            pool = untouched if not isinstance(transformation, SwapTransformation) else untouched
            result = transformation.apply(pool)

            touched = result if isinstance(result, tuple) else (result,)
            for tile in touched:
                if tile in untouched:
                    untouched.remove(tile)

            applied += 1

    # ------------------------------------------------------------------
    # Reassembly and lookup
    # ------------------------------------------------------------------

    def reassemble(self):
        canvas = self.original_image.copy()
        # sort by current_position so we place each tile where it NOW sits
        by_position = sorted(self.tiles, key=lambda t: t.current_position)

        for tile in by_position:
            row = tile.current_position // self.grid_size
            col = tile.current_position % self.grid_size
            y0 = row * self.tile_height
            x0 = col * self.tile_width
            canvas[y0:y0 + self.tile_height, x0:x0 + self.tile_width] = tile.get_display_image()

        return canvas

    def get_tile_at(self, x, y):
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

    def is_solved(self):
        return all(tile.is_correct() for tile in self.tiles)

    def incorrect_count(self):
        return sum(1 for tile in self.tiles if not tile.is_correct())

    def solve(self):
        for tile in self.tiles:
            tile.reset()