import numpy as np

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

    return (centroid_x, centroid_y)

if __name__ == "__main__":
    a = np.array([[1, 1, 0], [1, 0, 0], [0, 0, 0]])
    (x,y) = find_centroid(a)
    print("x coord: " + str(x) + ", y coord: " + str(y))