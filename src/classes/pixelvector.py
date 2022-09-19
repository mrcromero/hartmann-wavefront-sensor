import sys

# setting path
sys.path.append('./')

from .pixelcoords import PixelCoords

# Stores pixel vector between two PixelCoords
class PixelVector:
    x_vector = None
    y_vector = None

    def __init__(self, from_coords, to_coords):
        self.x_vector = to_coords.x - from_coords.x 
        self.y_vector = to_coords.y - from_coords.x