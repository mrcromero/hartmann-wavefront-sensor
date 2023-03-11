import numpy as np

# Create X and Y matrices
X, Y = np.meshgrid(np.arange(-3, 4), np.arange(-3, 4)[::-1])

# Create a mask for radius = 3.5 pixels
R = np.sqrt(X**2 + Y**2) <= 3.5

# Mask and normalize X, Y
X, Y = X*R, Y*R
X, Y = X/3.5, Y/3.5

coeff = np.array([
    0, # Z0
    0, # Z1
    0, # Z2
    0, # Z3
    4, # Z4
    0, # Z5
    0, # Z6
    0, # Z7
    0, # Z8
    0, # Z9
    0, # Z10
    0, # Z11
    0, # Z12
    0, # Z13
    0, # Z14
])

# dZ/dx partial derivative of Zernike polynomials
z_ders_x = [
    lambda x,y: (0),
    lambda x,y: (1),
    lambda x,y: (0),
    lambda x,y: (2*y),
    lambda x,y: (4*x),
    lambda x,y: (-2*x),#Z5
    lambda x,y: (3*y**2 - 3*x**2),
    lambda x,y: (-2 + 3*y**2 + 9*x**2),
    lambda x,y: (6*x*y),
    lambda x,y: (-6*x*y),
    lambda x,y: (4*y**3 - 12*x**2*y), #Z10
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
    lambda x,y: (2*y), # Z5
    lambda x,y: (6*x*y),
    lambda x,y: (6*x*y),
    lambda x,y: (-2 + 9*y**2 + 3*x**2),
    lambda x,y: (3*y**2 - 3*x**2),
    lambda x,y: (12*y**2*x - 4*x**3), # Z10
    lambda x,y: (-6*x + 24*y**2*x + 8*x**3),
    lambda x,y: (-12*y + 24*y**3 + 12*x**2*y),
    lambda x,y: (-6*y + 16*y**3 - 8*x**2*y ),
    lambda x,y: (4*y**3 - 12*x**2*y)
]

results_x = []
for c, func in zip(coeff, z_ders_x):
    result_x = c * np.vectorize(func)(X,Y)
    results_x.append(result_x)

x_displacement = np.sum(results_x, axis=0)
print(x_displacement)

results_y = []
for c, func in zip(coeff, z_ders_y):
    result_y = np.vectorize(func)(X,Y)
    results_y.append(result_y)

y_displacement = np.sum(results_y, axis=0)




