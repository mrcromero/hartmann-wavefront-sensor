import numpy as np

def zernike_displacement(coefficients):
    """
    Calculates the normalized x and y pixel displacements of 32-blobs based on a set of Zernike coefficients.
    The returned values should be multiplied by the actual radius (R) and rounded to the nearest integer before applying
    displacement shifts.

    Args:
    - coefficients (array-like): An array-like object containing the Zernike coefficients.

    Returns:
    - x_displacement (ndarray): A 7x7 2D array containing the x displacement of the wavefront at each pixel.
    - y_displacement (ndarray): A 7x7 2D array containing the y displacement of the wavefront at each pixel.
    """

    # Create X and Y matrices
    X, Y = np.meshgrid(np.arange(-3, 4), np.arange(-3, 4)[::-1])

    # Create a mask for radius = 3.5 pixels
    R = np.sqrt(X**2 + Y**2) <= 3.5

    # Mask X, Y for a circular pupil <= R
    X, Y = X*R, Y*R

    # Normalize X, Y
    X, Y = X*(236*3.5), Y*(236*3.5)

    # dZ/dx partial derivative of Zernike polynomials
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

    # dZ/dy partial derivative of Zernike polynomials
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

    # Calculate x displacement for given Zernike coefficients
    results_x = []
    for (c, func) in zip(coefficients, z_ders_x):
        result_x = c * np.vectorize(func)(X,Y)
        results_x.append(result_x)

    x_displacement = np.sum(results_x, axis = 0)

    # Calculate y displacement for given Zernike coefficients
    results_y = []
    for (c, func) in zip(coefficients, z_ders_y):
        result_y = c * np.vectorize(func)(X, Y)
        results_y.append(result_y)

    y_displacement = np.sum(results_y, axis = 0)

    # Return values
    return x_displacement, y_displacement


if __name__ == "__main__":
    # Test coefficient values
    coeff = np.array([
        0,  # Z0
        0,  # Z1
        0,  # Z2
        0,  # Z3
        0.005,  # Z4
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
    print(np.round(shift_x))
    # print(shift_y)
