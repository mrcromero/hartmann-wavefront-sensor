import sys
import pathlib
import cv2

# setting path
sys.path.append('/'.join(str(pathlib.Path(__file__).parent.resolve()).split('/')[:-1]))

from src.classes.zernikesolver import ZernikeSolver

def test_zernike_solver():
    x_vals = [0, 1, 2, 3]
    y_vals = [0, 1, 2, 3]
    v_vals = [0, 1, 2, 3, 4, 5, 6, 7]
    a = ZernikeSolver(x_array=x_vals, y_array=y_vals, v_array=v_vals)
    c = a.solve()
    for i in range(len(c)):
        print("C" + str(i) + ": " + str(c[i]))

if __name__ == "__main__":
    print("### Running Reconstruction Tests ###")
    test_zernike_solver()
    print("### All reconstruction tests passed! ###")