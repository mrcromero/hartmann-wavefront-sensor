import sys
import pathlib
import cv2

# setting path
sys.path.append('/'.join(str(pathlib.Path(__file__).parent.resolve()).split('/')[:-1]))

from src.classes.imagereader import ImageReader
from src.classes.imagedisplayer import ImageDisplayer
from src.classes.zernikesolver import ZernikeSolver

def test_init_image_reader():
    a = ImageReader('tests/images/Masked_100.bmp')
    assert a.grid is not None

    idisp = ImageDisplayer(a)

    print("# Displaying image and blobs #")
    cv2.imshow('Grid Image', idisp.get_grid_image())
    print("# Press a key to continue #")
    cv2.waitKey()
    cv2.destroyAllWindows()

def grid_vector_image():
    a = ImageReader('tests/images/Masked_100.bmp')

    idisp = ImageDisplayer(a)

    cv2.imshow('Regular Image', a.image)
    cv2.waitKey()
    print("# Displaying image and blobs #")
    cv2.imshow('Grid Image', idisp.get_vector_image())
    print("# Press a key to continue #")
    cv2.waitKey()
    cv2.destroyAllWindows()

def test_wavefront_recon():
    a = ImageReader('tests/images/Masked_100.bmp')
    idisp = ImageDisplayer(a)
    grid = a.grid

    cv2.imshow('Grid Image', idisp.get_vector_image())
    cv2.waitKey()
    cv2.destroyAllWindows()

    c = ZernikeSolver(grid).solve()
    for i in range(len(c)):
        print("C" + str(i) + ": " + str(c[i]))

if __name__ == "__main__":
    print("### Running Image Tests ###")
    #test_init_image_reader()
    #grid_vector_image()
    test_wavefront_recon()
    print("### All image tests passed! ###")