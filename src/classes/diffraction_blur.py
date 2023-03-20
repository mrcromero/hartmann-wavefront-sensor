import numpy as np
import matplotlib.pyplot as plt
from scipy.special import j1
from PIL import Image

from blobshift import zernike_displacement

"""
The CircularAperture class represents a circular aperture and can be used to compute and plot 
the diffraction pattern produced by the aperture.
"""
class CircularAperture:
    # @param diameter: diameter of the circular aperture
    def __init__(self, diameter, size,
                 shift_x=np.zeros((7,7)).astype(int),
                 shift_y=np.zeros((7,7)).astype(int)):
        self.diameter = diameter
        self.size = size
        self.shift_x = shift_x
        self.shift_y = shift_y
        
    # @param wavelength: wavelength of the light being diffracted [µm]
    # @param distance: distance from the aperture to the observation point [µm]
    # @return: 2D diffraction pattern

    def diffraction_pattern(self, wavelength, distance):
        k = 2 * np.pi / wavelength
        a = self.diameter / 2
        x = np.arange(-int(0.5*1.55*self.diameter), int(0.5*1.55*self.diameter)+1, 1)
        y = np.arange(-int(0.5*1.55*self.diameter), int(0.5*1.55*self.diameter)+1, 1)
        X, Y = np.meshgrid(x, y)
        R = np.sqrt(X**2 + Y**2)
        R[R==0] = np.finfo(float).eps
        pattern = (j1(k*R*a/distance)/(k*R*a/distance))**2
        pattern = pattern * 1E3
        return pattern
    
    # @param pattern: the 2D diffraction pattern returned by the diffraction_pattern method
    def plot_diffraction_pattern(self, pattern):
        plt.imshow(pattern, cmap='gray')
        plt.show()

    # Util function for applying shifts
    def apply_shift(self, pattern, x_index, y_index):
        cur_shift_x = self.shift_x[x_index][y_index]
        cur_shift_y = self.shift_y[x_index][y_index]
        
        padding_cols = [0] * abs(cur_shift_x)
        padding_cols = [padding_cols] * len(pattern)
        new_pattern = []
        x_start = 0
        x_end = len(pattern[0])
        y_start = 0
        y_end = len(pattern)

        if cur_shift_x < 0:
            new_pattern = np.hstack(tuple([pattern] + [padding_cols])) 
            x_start = abs(cur_shift_x)
            x_end = len(new_pattern[0])
        elif cur_shift_x > 0:
            new_pattern = np.hstack(tuple([padding_cols] + [pattern])) 
            x_start = 0
            x_end = len(pattern[0])
        else:
            new_pattern = pattern

        padding_rows = [0] * len(new_pattern[0])
        padding_rows = [padding_rows] * abs(cur_shift_y)
        if cur_shift_y < 0:
            new_pattern = np.vstack(tuple([padding_rows] + [new_pattern])) 
            y_start = 0
            y_end = len(pattern)
        elif cur_shift_y > 0:
            new_pattern = np.vstack(tuple([new_pattern]+ [padding_rows]))
            y_start = abs(cur_shift_y)
            y_end = len(new_pattern)
        new_pattern = np.asarray(new_pattern)[y_start:y_end, x_start:x_end]

        return new_pattern
    
    # Util function to add padding to the image in case of shifts to ensure
    # kernel does not go out of bounds during cross-correlation calculation
    def add_shift_padding(self, image):
        max_x_shift = max(np.absolute(np.reshape(self.shift_x, self.shift_x.size)))
        max_y_shift = max(np.absolute(np.reshape(self.shift_y, self.shift_y.size)))

        padding_cols = [0] * abs(max_x_shift)
        padding_cols = [padding_cols] * len(image)
        
        new_image = []
        if (max_x_shift != 0):
            new_image = np.hstack(tuple([padding_cols] + [image] + [padding_cols]))
        else:
            new_image = image
        
        padding_rows = [0] * len(new_image[0])
        padding_rows = [padding_rows] * abs(max_y_shift) 
        if (max_y_shift != 0):
            new_image = np.vstack(tuple([padding_rows] + [new_image] + [padding_rows]))
        return new_image


    def create_diffraction_grid(self, pattern):
        blob_pad = 1
        black_blob = np.zeros(pattern.shape)
        rows = [pattern]*self.size
        # Create row padding
        row_pad =  [black_blob] + [pattern]*(self.size-2*blob_pad) + [black_blob]
        cols = [row_pad] + [rows]*self.size + [row_pad]
        # Create column padding
        col_pad = [black_blob]*2 + [pattern]*(self.size-2*blob_pad) + [black_blob]*2
        image = []
        for i in range(len(cols)):
            cur_row = []
            cur_row.append(self.apply_shift(col_pad[i], i, 0))
            row_i = 1
            for j in range(len(cols[i])):
                cur_row.append(self.apply_shift(cols[i][j], i, row_i+j))
            cur_row.append(self.apply_shift(col_pad[i], i, -1))
            image.append(np.hstack(tuple(cur_row)))
        image = np.vstack(tuple(image))
        image = self.add_shift_padding(image)
        return image


if __name__ == "__main__":
    coeff = np.array([
        0,  # Z0
        0,  # Z1
        0,  # Z2
        0,  # Z3
        0.3,  # Z4
        0,  # Z5
        0,  # Z6
        0,  # Z7
        0,  # Z8
        0,  # Z9
        0,  # Z10
        0,  # Z11
        0,  # Z12
        0,  # Z13
        0,  # Z14
    ])
    shift_x, shift_y = zernike_displacement(coeff)

    ## Example for a 152.4µm diameter aperture, 3mm away, using 0.6µm wavelength light
    aperture = CircularAperture(152.4, 5, np.round(shift_x).astype(int), np.round(shift_y).astype(int))
    #aperture = CircularAperture(152.4, 5)
    pattern = aperture.diffraction_pattern(0.6, 20E3)
    #aperture.plot_diffraction_pattern(pattern)
    image = aperture.create_diffraction_grid(pattern)
    # Create the diffraction pattern plot

    # Save the plot as a .png file
    im = Image.fromarray(image).convert('RGB')
    im.save("diffraction_grid.png")
