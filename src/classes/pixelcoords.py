import sys

# setting path
sys.path.append('./')

# Stores pixel coordinates
class PixelCoords:
    x = None
    y = None

    def __init__(self, x, y):
        self.x = x
        self.y = y