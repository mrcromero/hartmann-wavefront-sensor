import sys

# setting path
sys.path.append('./')

import numpy as np
from .pixelcoords import PixelCoords

# A blob is a matrix of pixels with intensity values

class Blob:
    pixel_mat = None

    # pixel_mat is a NumPy array
    def __init__(self, pixel_mat):
        self.pixel_mat = pixel_mat
    
    # Finds the centroid in one NumPy array
    #
    # returns: a PixelCoords object containing the centroid of the blob
    def find_centroid(self):
        total_sum = np.sum(self.pixel_mat)
        weights_x = np.sum(self.pixel_mat, axis=0)/total_sum
        weights_y = np.sum(self.pixel_mat, axis=1)/total_sum

        centroid_x = 0
        for i in range(len(weights_x)):
            centroid_x += i*weights_x[i]

        centroid_y = 0
        for i in range(len(weights_y)):
            centroid_y += i*weights_y[i]

        return PixelCoords(centroid_x, centroid_y)