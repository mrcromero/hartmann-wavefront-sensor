import sys

# setting path
sys.path.append('../')

import numpy as np
from src.classes.blob import Blob
from src.classes.grid import Grid
from src.classes.pixelcoords import PixelCoords
from src.classes.pixelvector import PixelVector

def test_blob_centroid():
    a = np.array([[1, 1, 1], [1, 0, 0], [0, 0, 0]])
    test_blob = Blob(a)
    coords = test_blob.find_centroid()
    error_s = "Centroid coords x: {0}, y: {1}".format(coords.x, coords.y)
    assert coords.x == 0.75 and coords.y == 0.25, error_s

def test_grid_centroid():
    a = Blob(np.array([[1, 1, 1], [1, 0, 0], [0, 0, 0]]))
    b = Blob(np.array([[1, 0, 1], [1, 1, 0], [0, 0, 1]]))
    c = Blob(np.array([[0, 0, 0], [0, 0, 0], [0, 0, 0]]))
    d = Blob(np.array([[1, 1, 1], [1, 1, 1], [1, 1, 1]]))

    grid_matrix = [[],[]]
    grid_matrix[0].append(a)
    grid_matrix[0].append(b)
    grid_matrix[1].append(c)
    grid_matrix[1].append(d)

    grid = Grid(grid_matrix)

    grid.find_centroids()

# Tests for checking centroiding

if __name__ == "__main__":
    test_blob_centroid()
    test_grid_centroid()
    print("All tests passed!")