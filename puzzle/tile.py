#Hit137 Software Now
#Assessment3 - Image Puzzle Game
#Riwaj Shrestha (403312)
#Sawan Gurung (407504)
#Jung-Chuan Chiang (406089)

import cv2


class Tile:
    def __init__(self, image, correct_position, tile_id):
        self._original_image = image.copy()
        self._correct_position = correct_position
        self._current_position = correct_position
        self._tile_id = tile_id

        self._rotation = 0        
        self._mirrored = False
        

    @property
    def current_position(self):
        return self._current_position

    @current_position.setter
    def current_position(self, position):
        self._current_position = position

    @property
    def correct_position(self):
        return self._correct_position

    def apply_rotation(self, degrees):
        self._rotation = (self._rotation + degrees) % 360

    def apply_flip(self, horizontal=False, vertical=False):

        if horizontal:
            self._flip_displayed_horizontally()

        if vertical:
            self._flip_displayed_horizontally()
            self.apply_rotation(180)

    def _flip_displayed_horizontally(self):
        self._mirrored = not self._mirrored
        self._rotation = (-self._rotation) % 360

    @property
    def tile_id(self):
        return self._tile_id

    def reset(self):
        self._current_position = self._correct_position
        self._rotation = 0
        self._mirrored = False

    def get_display_image(self):
        image = self._original_image

        if self._mirrored:
            image = cv2.flip(image, 1)

        if self._rotation == 90:
            image = cv2.rotate(image, cv2.ROTATE_90_CLOCKWISE)
        elif self._rotation == 180:
            image = cv2.rotate(image, cv2.ROTATE_180)
        elif self._rotation == 270:
            image = cv2.rotate(image, cv2.ROTATE_90_COUNTERCLOCKWISE)

        return image

    def is_correct(self):
        return (
            self._current_position == self._correct_position
            and self._rotation == 0
            and not self._mirrored
        )
