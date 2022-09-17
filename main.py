import numpy as np

import src.find_centroid as fc

# Tests
if __name__ == "__main__":
    a = np.array([[1, 1, 0], [1, 0, 0], [0, 0, 0]])
    coords = fc.find_centroid(a)
    print("x coord: " + str(coords.x) + ", y coord: " + str(coords.y))