import numpy as np

class PixelCoords:
    x = None
    y = None

    def __init__(self, x, y):
        self.x = x
        self.y = y


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

def centroid_grid(grid):
    c_grid = []

    for i in range(len(grid)):
        c_grid.append([])
        for j in range(len(grid[0])):
            blob = grid[i][j]
            c_pixels = find_centroid(blob)
            c_grid[i].append(c_pixels)

    return c_grid

if __name__ == "__main__":
    a = np.array([[1, 1, 0], [1, 0, 0], [0, 0, 0]])
    coords = find_centroid(a)
    print("x coord: " + str(coords.x) + ", y coord: " + str(coords.y))