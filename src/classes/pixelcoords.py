import sys

# setting path
sys.path.append('./')

# Stores pixel coordinates
# Rounds pixel coordinates to 3 decimal points to ensure no floating point
# arithmetic errors occur
class PixelCoords:
    x = None
    y = None

    def __init__(self, x, y):
        self.x = round(x, 3)
        self.y = round(y, 3)