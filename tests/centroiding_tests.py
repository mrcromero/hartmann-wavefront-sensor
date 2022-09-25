import sys
import pathlib


# setting path
sys.path.append('/'.join(str(pathlib.Path(__file__).parent.resolve()).split('/')[:-1]))

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

    centroids = grid.find_centroids()

    answers = [[(0.75, 0.25), (1, 0.8)], [(1, 1), (1, 1)]]

    for i in range(len(centroids)):
        for j in range(len(centroids[i])):
            coords = centroids[i][j]
            a = answers[i][j]
            error_s = "Centroid coords for [{0},{1}] -- x: {2}, y: {3}".format(
                i, j, coords.x, coords.y)
            assert coords.x == a[0] and coords.y == a[1], error_s


# Tests for checking centroiding

if __name__ == "__main__":
    test_blob_centroid()
    test_grid_centroid()
    print("All tests passed!")