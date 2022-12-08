import sys
import pathlib
import cv2

# setting path
sys.path.append('/'.join(str(pathlib.Path(__file__).parent.resolve()).split('/')[:-1]))

from src.classes.zernikesolver import ZernikeSolver

x_vals = [0, 1, 2, 3]
y_vals = [0, 1, 2, 3]
xv_vals = [0, 1, 2, 3]
yv_vals = [4, 5, 6, 7]
control_c = []


def test_zernike_solver():
    v_vals = xv_vals+yv_vals
    a = ZernikeSolver(x_array=x_vals, y_array=y_vals, v_array=v_vals)
    global control_c
    control_c = a.solve()
    assert len(control_c) == 15, "%s coefficients found" % len(control_c)
    
def test_zernike_xshift():
    print("   # Testing change in x-tilt")
    new_xv_vals = [xv + 1 for xv in xv_vals]
    v_vals = new_xv_vals+yv_vals
    a = ZernikeSolver(x_array=x_vals, y_array=y_vals, v_array=v_vals)
    c = a.solve()
    test_c = c[0] + c[2:]
    test_control = control_c[0] + control_c[2:]
    equalities = [test_c[i] == test_control[i] for i in range(len(test_c))]
    assert all(equalities), "incorrect coefficients have changed"

def test_zernike_yshift():
    print("   # Testing change in y-tilt")
    new_yv_vals = [yv + 1 for yv in yv_vals]
    v_vals = xv_vals+new_yv_vals
    a = ZernikeSolver(x_array=x_vals, y_array=y_vals, v_array=v_vals)
    c = a.solve()
    test_c = c[0] + c[2:]
    test_control = control_c[0] + control_c[2:]
    equalities = [test_c[i] == test_control[i] for i in range(len(test_c))]
    assert all(equalities), "incorrect coefficients have changed"

if __name__ == "__main__":
    print("### Running Reconstruction Tests ###")
    test_zernike_solver()
    test_zernike_xshift()
    print("### All reconstruction tests passed! ###")