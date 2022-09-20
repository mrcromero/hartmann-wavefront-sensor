import sys

# setting path
sys.path.append('./')

import numpy as np
from .pixelcoords import PixelCoords
from .pixelvector import PixelVector

# A blob is a matrix of pixels with intensity values

class Blob:
    pixel_mat = None
    middle_coords = None
    centroid_coords = None

    # pixel_mat is a NumPy array
    def __init__(self, pixel_mat):
        self.pixel_mat = pixel_mat
        middle_x = len(pixel_mat)/2
        middle_y = len(pixel_mat[0])/2
        self.middle_coords = PixelCoords(middle_x, middle_y)
    
    # Finds the centroid Blob's centroid if it isn't defined. Otherwise,
    # calculate and store it
    #
    # returns: a PixelCoords object containing the centroid of the blob
    def find_centroid(self):
        if self.centroid_coords == None:
            total_sum = np.sum(self.pixel_mat)
            weights_x = np.sum(self.pixel_mat, axis=0)/total_sum
            weights_y = np.sum(self.pixel_mat, axis=1)/total_sum

            centroid_x = 0
            for i in range(len(weights_x)):
                centroid_x += i*weights_x[i]

            centroid_y = 0
            for i in range(len(weights_y)):
                centroid_y += i*weights_y[i]
            self.centroid_coords = PixelCoords(centroid_x, centroid_y)

        return self.centroid_coords

    # Returns the vector from the blob's middle to its centroid
    def find_vector_to_centroid(self):
        return PixelVector(self.middle_coords, self.centroid_coords)
