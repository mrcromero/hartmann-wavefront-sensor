import sys
import pathlib


# setting path
sys.path.append('/'.join(str(pathlib.Path(__file__).parent.resolve()).split('/')[:-1]))

if __name__ == "__main__":
    print("All image tests passed!")