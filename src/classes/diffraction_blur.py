import numpy as np
import matplotlib.pyplot as plt
from scipy.special import j1
"""
The CircularAperture class represents a circular aperture and can be used to compute and plot 
the diffraction pattern produced by the aperture.
"""
class CircularAperture:
    # @param diameter: diameter of the circular aperture
    def __init__(self, diameter):
        self.diameter = diameter
        
    # @param wavelength: wavelength of the light being diffracted [µm]
    # @param distance: distance from the aperture to the observation point [µm]
    # @return: 2D diffraction pattern

    def diffraction_pattern(self, wavelength, distance):
        k = 2 * np.pi / wavelength
        a = self.diameter / 2
        x = np.linspace(-0.5*a, 0.5*a, 1000)
        y = np.linspace(-0.5*a, 0.5*a, 1000)
        X, Y = np.meshgrid(x, y)
        R = np.sqrt(X**2 + Y**2)
        pattern = (j1(k*R*a/distance)/(k*R*a/distance))**2
        pattern = pattern * 255/np.amax(pattern)
        return pattern
    
    # @param pattern: the 2D diffraction pattern returned by the diffraction_pattern method
    def plot_diffraction_pattern(self, pattern):
        plt.imshow(pattern, cmap='gray')
        plt.show()

## Example for a 152.4µm diameter aperture, 3mm away, using 0.6µm wavelength light
aperture = CircularAperture(152.4) 
pattern = aperture.diffraction_pattern(0.6, 3E3)
aperture.plot_diffraction_pattern(pattern)