import numpy as np
import matplotlib.pyplot as plt
from scipy.special import j1
from PIL import Image
"""
The CircularAperture class represents a circular aperture and can be used to compute and plot 
the diffraction pattern produced by the aperture.
"""
class CircularAperture:
    # @param diameter: diameter of the circular aperture
    def __init__(self, diameter, size):
        self.diameter = diameter
        self.size = size
        
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

    def create_diffraction_grid(self, pattern):
        blob_pad = 1
        black_blob = np.zeros(pattern.shape)
        row_pattern = []
        rows = [pattern]*self.size
        row_pattern = np.hstack(tuple(rows))
        # Create row padding
        row_pad =  np.hstack(tuple([black_blob] + [pattern]*(self.size-2*blob_pad) + [black_blob]))
        cols = [row_pad] + [row_pattern]*self.size + [row_pad]
        # Create column padding
        col_pad = np.vstack(tuple([black_blob]*2 + [pattern]*(self.size-2*blob_pad) + [black_blob]*2))
        diff_grid = np.hstack(tuple([col_pad] + [np.vstack(tuple(cols))] + [col_pad]))
        plt.imshow(diff_grid, cmap='gray')
        plt.show()
        return diff_grid

## Example for a 152.4µm diameter aperture, 3mm away, using 0.6µm wavelength light
aperture = CircularAperture(152.4, 5) 
pattern = aperture.diffraction_pattern(0.6, 3E3)
aperture.plot_diffraction_pattern(pattern)
# Create the diffraction pattern plot

# Save the plot as a .png file
plt.savefig('diffraction_pattern.png')