import numpy as np

from .grid import Grid

# Class for wavefront reconstruction via Modal Wave-Front Estimation from
# Local Slopes
class ZernikeSolver:
    grid = None
    coeffs = 0
    coord_array_x = []
    coord_array_y = []
    vector_array =  []
    t_matrix = []

    # array options are for testing
    def __init__(self, grid=None, x_array=None, y_array=None, v_array=None, coeffs=15):
        # If grid is none, then set to testing mode
        self.coeffs = coeffs
        if (grid == None):
            self.coord_array_x = x_array
            self.coord_array_y = y_array
            self.vector_array = v_array
        else:
            self.grid = grid
            self.grid_coord_to_array()
            self.grid_vecs_to_array()
        self.calc_t_matrix()

    # Converts the coordinates of the grid to an array for x and y
    def grid_coord_to_array(self):
        blob_vec = self.grid.blob_mat
        self.coord_array_x = [(b.i_center_coords.x)/(3.5*236) for b in blob_vec]
        self.coord_array_y = [(b.i_center_coords.y)/(3.5*236)  for b in blob_vec]

    # Gets the vectors of a grid and converts it to an array
    def grid_vecs_to_array(self):
        vecs = self.grid.find_vectors_to_centroids()
        self.vector_array = ((np.array([v.x_vector for v in vecs] + [v.y_vector for v in vecs])))
        # divided by mask-sensor distance and multiplied by pixel length 
        self.vector_array /= - 20E3
        self.vector_array *= 1.55
        
    # Calculates the transformation matrix for wavefront reconstruction
    # Zernike Polynomials Z(x,y) to the 4th Degree:
    #   - Z0 = 1
    #   - Z1 = x
    #   - Z2 = y
    #   - Z3 = 2*x*y
    #   - Z4 = -1 + 2*y**2 + 2*x**2
    #   - Z5 = y**2 - x**2
    #   - Z6 = 3*x*y**2 - x**3
    #   - Z7 = -2*x + 3*x*y**2 + 3*x**3
    #   - Z8 = -2*y + 3*y**3 + 3*x**2*y
    #   - Z9 = y**3 - 3*x**2*y
    #   - Z10 = 4*y**3*x - 4*x**3*y
    #   - Z11 = -6*x*y + 8*y**3*x + 8*x**3*y
    #   - Z12 = 1 - 6*y**2 - 6*x**2 + 6*y**4 + 12*x**2*y**2 + 6*x**4
    #   - Z13 = -3*y**2 + 3*x**2 + 4*y**4 - 4*x**2*y**2 - 4*x**4
    #   - Z14 = y**4 - 6*x**2*y**2 + x**4
    def calc_t_matrix(self):
        t_matrix_t = []
        num_c = 16 if self.coeffs >= 15 else self.coeffs
        # Partial derivatives of x of Zernike polynomials
        z_ders_x = [
            lambda x,y: (0),
            lambda x,y: (1),
            lambda x,y: (0),
            lambda x,y: (2*y),
            lambda x,y: (4*x),
            lambda x,y: (-2*x),
            lambda x,y: (3*y**2 - 3*x**2),
            lambda x,y: (-2 + 3*y**2 + 9*x**2),
            lambda x,y: (6*x*y),
            lambda x,y: (-6*x*y),
            lambda x,y: (4*y**3 - 12*x**2*y),
            lambda x,y: (-6*y + 8*y**3 + 24*x**2*y),
            lambda x,y: (-12*x + 24*x*y**2 + 24*x**3),
            lambda x,y: (6*x - 8*x*y**2 - 16*x**3),
            lambda x,y: (-12*x*y**2 + 4*x**3)
        ]

        # Partial derivatives of y of Zernike polynomials
        z_ders_y = [
            lambda x,y: (0),
            lambda x,y: (0),
            lambda x,y: (1),
            lambda x,y: (2*x),
            lambda x,y: (4*y),
            lambda x,y: (2*y),
            lambda x,y: (6*x*y),
            lambda x,y: (6*x*y),
            lambda x,y: (-2 + 9*y**2 + 3*x**2),
            lambda x,y: (3*y**2 - 3*x**2),
            lambda x,y: (12*y**2*x - 4*x**3),
            lambda x,y: (-6*x + 24*y**2*x + 8*x**3),
            lambda x,y: (-12*y + 24*y**3 + 12*x**2*y),
            lambda x,y: (-6*y + 16*y**3 - 8*x**2*y ),
            lambda x,y: (4*y**3 - 12*x**2*y)
        ]
        for i in range(num_c):
            zx = z_ders_x[i]
            zy = z_ders_y[i]
            t_matrix_t.append(
                [j for j in map(zx, self.coord_array_x, self.coord_array_y)] + 
                [j for j in map(zy, self.coord_array_x, self.coord_array_y)]
            )
        self.t_matrix = np.array(t_matrix_t).transpose()

    # Solves wavefront reconstruction and returns the Zernike coefficients
    #
    # returns: a vector of the coefficients of the Zernike functions which
    #          characterizes the light wave
    def solve(self):
        return np.matmul(np.linalg.pinv(self.t_matrix), self.vector_array) 