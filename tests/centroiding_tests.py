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
    assert coords.x == 1 and coords.y == 1, error_s

def test_grid_centroid():
    a = Blob(np.array([[1, 1, 1], [1, 0, 0], [0, 0, 0]]))
    b = Blob(np.array([[1, 0, 1], [1, 1, 0], [0, 0, 1]]))
    c = Blob(np.array([[0, 0, 0], [0, 0, 0], [0, 0, 0]]))
    d = Blob(np.array([[1, 1, 1], [1, 1, 1], [1, 1, 1]]))

    grid_matrix = [a,b,c,d]
    grid = Grid(grid_matrix)

    centroids = grid.find_centroids()

    answers = [(1, 1), (1, 1), (1, 1), (1, 1)]

    for i in range(len(centroids)):
        coords = centroids[i]
        a = answers[i]
        error_s = "Centroid coords for [{0}] -- x: {1}, y: {2}".format(
            i, coords.x, coords.y)
        assert coords.x == a[0] and coords.y == a[1], error_s

def test_blob_vectoring():
    a = np.array([[1, 1, 1], [1, 0, 0], [0, 0, 0]])
    test_blob = Blob(a)
    vector = test_blob.find_vector_to_centroid()
    error_s = "Vector distances x: {0}, y: {1}".format(
        vector.x_vector, vector.y_vector)
    assert vector.x_vector == 0 and vector.y_vector == 0, error_s
    assert vector.x_length == 0 and vector.y_length == 0, error_s

def test_grid_vectoring():
    a = Blob(np.array([[1, 1, 1], [1, 0, 0], [0, 0, 0]]))
    b = Blob(np.array([[1, 0, 1], [1, 1, 0], [0, 0, 1]]))
    c = Blob(np.array([[0, 0, 0], [0, 0, 0], [0, 0, 0]]))
    d = Blob(np.array([[1, 1, 1], [1, 1, 1], [1, 1, 1]]))

    grid_matrix = [a,b,c,d]

    grid = Grid(grid_matrix)

    vectors = grid.find_vectors_to_centroids()

    answers_v = [(0, 0), (0, 0), (0, 0), (0, 0)]
    answers_l = [(0, 0), (0, 0), (0, 0), (0, 0)]

    for i in range(len(vectors)):
        v = vectors[i]
        a_v = answers_v[i]
        a_l = answers_l[i]
        error_s = "Vector distances for [{0}] -- x: {1}, y: {2}".format(
            i, v.x_vector, v.y_vector)
        assert v.x_vector == a_v[0] and v.y_vector == a_v[1], error_s
        assert v.x_length == a_l[0] and v.y_length == a_l[1], error_s


# Tests for checking centroiding

if __name__ == "__main__":
    print("### Running Centroiding Tests ###")
    test_blob_centroid()
    test_grid_centroid()
    test_blob_vectoring()
    test_grid_vectoring()
    print("### All centroiding tests passed! ###")