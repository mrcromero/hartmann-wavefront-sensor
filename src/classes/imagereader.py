import sys
import cv2

# setting path
sys.path.append('./')

from .grid import Grid
from .blob import Blob

class ImageReader:
    image = None
    center_x = None
    center_y = None
    grid = None

    # The way the init works is subject to change depending on how image
    # streaming works
    # Regardless, would like to have an optional 'path' variable for testing
    # single images
    def __init__(self, path):
        self.image = cv2.cvtColor(cv2.imread(path), cv2.COLOR_BGR2GRAY)
        center_x = sum([i for i in range(len(self.image))])/len(self.image)
        center_y = sum([i for i in range(len(self.image[0]))])/len(self.image[0])
        self.get_grid()

    def get_grid(self, x=center_x, y=center_y):
        if self.grid != None:
            if x != self.center_x or y != self.center_y:
                self.center_x = x
                self.center_y = y
            else:
                return self.grid
        # Calculate grid using center_x and center_y and place in grid
        grid = Grid()
        self.grid = grid
        return grid

    def update_grid(self, delta_x, delta_y):
        new_x = self.center_x + delta_x
        new_y = self.center_y + delta_y
        if (new_x < 0 or new_x > len(self.image) or
            new_y < 0 or new_y > len(self.image)):
            return self.get_grid()
        return self.get_grid(new_x, new_y)