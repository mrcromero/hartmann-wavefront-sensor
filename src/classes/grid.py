import sys
import numpy as np
import cv2

# setting path
sys.path.append('./')


# A grid is a matrix of Blobs
class Grid:
    blob_mat = None

    def __init__(self, blob_mat):
        self.blob_mat = blob_mat
    
    # Finds the centroids of each blob array in the grid
    #
    # returns: a 2D array where each element is a PixelCoords object
    #          storing the centroid of their respective NumPy array
    def find_centroids(self):
        c_grid = []

        for i in range(len(self.blob_mat)):
            c_grid.append([])
            for j in range(len(self.blob_mat[0])):
                blob = self.blob_mat[i][j]
                c_pixels = blob.find_centroid()
                c_grid[i].append(c_pixels)

        return c_grid

    # Finds the vectors to centroids of each blob array in the grid
    #
    # returns: a 2D array where each element is a PixelVector object
    #          storing the vector to centroid of their respective NumPy array
    def find_vectors_to_centroids(self):
        v_grid = []

        for i in range(len(self.blob_mat)):
            v_grid.append([])
            for j in range(len(self.blob_mat[0])):
                blob = self.blob_mat[i][j]
                c_vector = blob.find_vector_to_centroid()
                v_grid[i].append(c_vector)

        return v_grid

    # Concatenates all the blobs in the grid into a single numpy array.
    # Also adds grid lines to show blob grids
    def get_grid_image(self):
        concat_grid = []
        for i in range(len(self.blob_mat)):
            cur_row = []
            for j in range(len(self.blob_mat[0])):
                gray_blob = self.blob_mat[i][j].pixel_mat
                cur_blob = cv2.cvtColor(gray_blob,cv2.COLOR_GRAY2RGB)
                # Add grid lines
                cur_blob[0,:,0] = 255
                cur_blob[-1,:,0] = 255
                cur_blob[:,0,0] = 255
                cur_blob[:,-1,0] = 255
                cur_row.append(cur_blob)
            concat_grid.append(np.hstack(tuple(cur_row)))
        grid_image = np.vstack(tuple(concat_grid))
        # Add grid lines
        grid_image[0:2,:,0] = 255
        grid_image[-3:-1,:,0] = 255
        grid_image[:,0:2,0] = 255
        grid_image[:,-3:-1,0] = 255
        return grid_image
    