import numpy as np

from .grid import Grid

# Class for wavefront reconstruction via Modal Wave-Front Estimation from
# Local Slopes
class ZernikeSolver:
    grid: Grid = None
    coord_array_x = []
    coord_array_y = []
    vector_array =  []
    t_matrix = []

    def __init__(self, grid: Grid, blob_size, ap_size):
        self.grid = grid
        self.grid_coord_to_array()
        self.grid_vecs_to_array()
        self.calc_t_matrix()

    # Converts the coordinates of the grid to an array for x and y
    def grid_coord_to_array(self):
        blob_vec = np.reshape(self.grid.blob_mat, (self.grid.size))
        self.coord_array_x = [b.i_center_coords.x for b in blob_vec]
        self.coord_array_y = [b.i_center_coords.y for b in blob_vec]

    # Gets the vectors of a grid and converts it to an array
    def grid_vecs_to_array(self):
        vecs = np.reshape(self.grid.find_vectors_to_centroids(), (self.grid.size))
        self.vector_array = [v.x_length for v in vecs] + [v.y_length for v in vecs]

    # Calculates the transformation matrix for wavefront reconstruction
    def calc_t_matrix(self):
        # Partial derivatives of x of Zernike functions
        z_ders_x = [
            lambda x,y: (x+y),
            lambda x,y: (x+y),
            lambda x,y: (x+y),
            lambda x,y: (x+y),
            lambda x,y: (x+y),
            lambda x,y: (x+y),
            lambda x,y: (x+y),
            lambda x,y: (x+y),
            lambda x,y: (x+y),
            lambda x,y: (x+y),
            lambda x,y: (x+y),
            lambda x,y: (x+y),
            lambda x,y: (x+y),
            lambda x,y: (x+y)
        ]

        # Partial derivatives of y of Zernike functions
        z_ders_y = [
            lambda x,y: (x-y),
            lambda x,y: (x-y),
            lambda x,y: (x-y),
            lambda x,y: (x-y),
            lambda x,y: (x-y),
            lambda x,y: (x-y),
            lambda x,y: (x-y),
            lambda x,y: (x-y),
            lambda x,y: (x-y),
            lambda x,y: (x-y),
            lambda x,y: (x-y),
            lambda x,y: (x-y),
            lambda x,y: (x-y),
            lambda x,y: (x-y)
        ]
        for i in range(14):
            zx = z_ders_x[i]
            zy = z_ders_y[i]
            self.t_matrix.append(
                [j for j in map(zx, self.coord_array_x, self.coord_array_y)] + 
                [j for j in map(zy, self.coord_array_x, self.coord_array_y)]
            )

    # Solves wavefront reconstruction and returns the Zernike coefficients
    #
    # returns: a vector of the coefficients of the Zernike functions which
    #          describes the light wave
    def solve(self):
        return np.matmul(self.t_matrix, self.vector_array)