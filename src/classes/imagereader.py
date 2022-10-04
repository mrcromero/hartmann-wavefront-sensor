import sys
import cv2

# setting path
sys.path.append('./')

from .grid import Grid
from .blob import Blob

class ImageReader:
    blob_size = 0
    grid_size = 0
    image = None
    center_x = None
    center_y = None
    grid = None

    # The way the init works is subject to change depending on how image
    # streaming works
    # Regardless, would like to have an optional 'path' variable for testing
    # single images
    # Default values:
    #   - for Blobs is 140x140 pixels
    #   - for Grids is 7x7 Blobs
    def __init__(self, path, blob_size=140, grid_size=7):
        self.image = cv2.cvtColor(cv2.imread(path), cv2.COLOR_BGR2GRAY)
        self.center_x = len(self.image[0])//2
        self.center_y = len(self.image)//2
        self.blob_size = blob_size
        self.grid_size = grid_size
        self.get_grid()

    def get_grid(self, x=None, y=None):
        if self.grid != None:
            if x != None or y != None:
                self.center_x = x
                self.center_y = y
            else:
                return self.grid
        # Calculate grid using center_x and center_y and place in grid
        
        grid = Grid([])
        self.grid = grid
        return grid

    def update_grid(self, delta_x, delta_y):
        length_to_edge = (self.grid_size/2) * self.blob_size
        new_x = self.center_x + delta_x
        new_y = self.center_y + delta_y
        if (new_x-length_to_edge < 0 or
            new_x+length_to_edge > len(self.image)-1 or
            new_y-length_to_edge < 0 or
            new_y+length_to_edge > len(self.image)-1):
            return self.get_grid()
        return self.get_grid(new_x, new_y)