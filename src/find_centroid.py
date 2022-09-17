import numpy as np

# Stores pixel coordinates
class PixelCoords:
    x = None
    y = None

    def __init__(self, x, y):
        self.x = x
        self.y = y

# Finds the centroid in one NumPy array
#
# params:
#   - arr: NumPy array to find the centroid of
#
# returns: a PixelCoords object containing the centroid of arr
def find_centroid(arr):
    total_sum = np.sum(arr)
    weights_x = np.sum(arr, axis=0)/total_sum
    weights_y = np.sum(arr, axis=1)/total_sum

    centroid_x = 0
    for i in range(len(weights_x)):
        centroid_x += i*weights_x[i]

    centroid_y = 0
    for i in range(len(weights_y)):
        centroid_y += i*weights_y[i]

    return PixelCoords(centroid_x, centroid_y)

# Finds the centroids of each NumPy array in a grid
#
# params:
#   - grid: 2D array where each element is a separate 2D NumPy array
# returns: a 2D array where each element is a PixelCoords object
#          storing the centroid of their respective NumPy array
def centroid_grid(grid):
    c_grid = []

    for i in range(len(grid)):
        c_grid.append([])
        for j in range(len(grid[0])):
            blob = grid[i][j]
            c_pixels = find_centroid(blob)
            c_grid[i].append(c_pixels)

    return c_grid