import sys

# setting path
sys.path.append('./')

from .pixelcoords import PixelCoords

# Stores pixel vector between two PixelCoords
#
# Rounds to 3 decimal points to remove any ambigquity due to floating
# point arithmetic
class PixelVector:
    x_vector = None
    y_vector = None

    def __init__(self, from_coords, to_coords, pixel_length=0):
        self.x_vector = round(to_coords.x - from_coords.x, 3)
        self.y_vector = round(to_coords.y - from_coords.y, 3)