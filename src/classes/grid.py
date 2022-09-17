
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