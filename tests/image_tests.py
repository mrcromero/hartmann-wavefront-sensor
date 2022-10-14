import sys
import pathlib
import cv2

# setting path
sys.path.append('/'.join(str(pathlib.Path(__file__).parent.resolve()).split('/')[:-1]))

from src.classes.imagereader import ImageReader

def test_init_image_reader():
    a = ImageReader('tests/images/100.bmp')
    assert a.get_grid() is not None

    grid = a.get_grid()

    print("# Displaying image and blobs #")
    cv2.imshow('Grid Image', grid.get_grid_image())
    print("# Press a key to continue #")
    cv2.waitKey()
    cv2.destroyAllWindows()

def grid_vector_image():
    a = ImageReader('tests/images/200.bmp')

    grid = a.get_grid()

    print("# Displaying image and blobs #")
    cv2.imshow('Grid Image', grid.get_vector_image())
    print("# Press a key to continue #")
    cv2.waitKey()
    cv2.destroyAllWindows()


if __name__ == "__main__":
    print("### Running Image Tests ###")
    test_init_image_reader()
    grid_vector_image()
    print("### All image tests passed! ###")