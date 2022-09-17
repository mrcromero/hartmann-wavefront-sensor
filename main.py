import numpy as np
from src.classes.blob import Blob
from src.classes.grid import Grid
from src.classes.pixelcoords import PixelCoords
from src.classes.pixelvector import PixelVector

# Tests
if __name__ == "__main__":
    a = np.array([[1, 1, 0], [1, 0, 0], [0, 0, 0]])
    test_blob = Blob(a)
    coords = test_blob.find_centroid()
    print("x coord: " + str(coords.x) + ", y coord: " + str(coords.y))