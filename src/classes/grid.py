import sys
import numpy as np
import cv2

# setting path
sys.path.append('./')


# A grid is a matrix of Blobs
class Grid:
    blob_mat = None
    size = 0

    def __init__(self, blob_mat):
        self.blob_mat = blob_mat
        self.size = blob_mat
    
    # Finds the centroids of each blob array in the grid
    #
    # returns: a 1D array where each element is a PixelCoords object
    #          storing the centroid of their respective NumPy array
    def find_centroids(self):
        cents = []

        for i in range(len(self.blob_mat)):
            blob = self.blob_mat[i]
            c_pixels = blob.find_centroid()
            cents.append(c_pixels)


        return cents

    # Finds the vectors to centroids of each blob array in the grid
    #
    # returns: a 2D array where each element is a PixelVector object
    #          storing the vector to centroid of their respective NumPy array
    def find_vectors_to_centroids(self):
        vecs = []

        for i in range(len(self.blob_mat)):
            blob = self.blob_mat[i]
            c_vector = blob.find_vector_to_centroid()
            vecs.append(c_vector)

        return vecs
    