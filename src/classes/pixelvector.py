import sys

# setting path
sys.path.append('./')

from .pixelcoords import PixelCoords

# Stores pixel vector between two PixelCoords
class PixelVector:
    pixel_length = 0
    x_vector = None
    y_vector = None
    x_pixels = None
    y_pixels = None

    def __init__(self, from_coords, to_coords, pixel_length=1.55):
        self.x_vector = to_coords.x - from_coords.x 
        self.y_vector = to_coords.y - from_coords.x
        self.pixel_length = pixel_length
        self.x_pixels = self.x_vector*pixel_length
        self.y_pixels = self.y_vector*pixel_length