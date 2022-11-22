import numpy as np

# Class for wavefront reconstruction via Modal Wave-Front Estimation from
# Local Slopes
class ZernikeSolver:
    grid = None
    coord_array = None
    vector_array =  None
    t_matrix = None

    def __init__(self, grid, blob_size, ap_size):
        self.grid = grid
        self.grid_coord_to_array()
        self.grid_vecs_to_array()
        self.calc_t_matrix()

    # Converts the coordinates of the grid to an array
    def grid_coord_to_array(self):
        self.vector_array = None

    # Gets the vectors of a grid and converts it to a vector
    def grid_vecs_to_array(self):
        self.vector_array = None

    # Calculates the transformation matrix for wavefront reconstruction
    def calc_t_matrix(self):
        self.t_matrix = None

    # Solves wavefront reconstruction and returns the Zernike coefficients
    def solve(self):
        return np.divide(self.vector_array, self.t_matrix)