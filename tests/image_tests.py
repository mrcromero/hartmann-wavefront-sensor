import sys
import pathlib

# setting path
sys.path.append('/'.join(str(pathlib.Path(__file__).parent.resolve()).split('/')[:-1]))

from src.classes.imagereader import ImageReader

def test_init_image_reader():
    a = ImageReader('tests/images/100.bmp')
    assert a.get_grid() is not None

if __name__ == "__main__":
    test_init_image_reader()
    print("All image tests passed!")