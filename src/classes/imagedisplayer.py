import sys
import cv2
import numpy as np
import pandas as pd

# setting path
sys.path.append('./')

from .grid import Grid
from .blob import Blob
from .imagereader import ImageReader

# Just a utility class for displaying images
class ImageDisplayer:
    grid = None
    image = None

    def __init__(self, imagereader):
        self.grid = imagereader.grid
        self.image =cv2.cvtColor(imagereader.image,cv2.COLOR_GRAY2RGB) 

    # Concatenates all the blobs in the grid into a single numpy array.
    # Also adds grid lines to show blob grids
    def get_grid_image(self):
        blobs = self.grid.blob_mat
        masked_image = self.image.copy()
        for i in range(len(blobs)):
            blob = blobs[i]
            center_x, center_y = round(blob.center_coords.x), round(blob.center_coords.y)
            gray_blob = blob.pixel_mat
            cur_blob = cv2.cvtColor(gray_blob,cv2.COLOR_GRAY2RGB)
            rad = cur_blob.shape[0]//2
            # Add grid lines
            masked_image[center_x-rad,center_y-rad:center_y+rad,0] = 255
            masked_image[center_x+rad,center_y-rad:center_y+rad,0] = 255
            masked_image[center_x-rad:center_x+rad,center_y-rad,0] = 255
            masked_image[center_x-rad:center_x+rad,center_y+rad,0] = 255
        return masked_image

    # Gets the grid like get_grid_images, but also adds approximate centroid
    # location and vectors
    def get_vector_image(self):
        blobs = self.grid.blob_mat
        masked_image = self.image.copy()
        # set values for vector drawing
        arrow_color  = (0, 0, 255)
        thickness = 2
        for i in range(len(blobs)):
            blob = blobs[i]
            center_x, center_y = round(blob.center_coords.x), round(blob.center_coords.y)
            centroid_x, centroid_y = round(blob.find_centroid().x), round(blob.find_centroid().y)
            gray_blob = blob.pixel_mat
            cur_blob = cv2.cvtColor(gray_blob,cv2.COLOR_GRAY2RGB)
            rad = cur_blob.shape[0]//2
            init_x, init_y = center_x-rad, center_y-rad

            # Add grid lines
            masked_image[center_x-rad,center_y-rad:center_y+rad,0] = 255
            masked_image[center_x+rad,center_y-rad:center_y+rad,0] = 255
            masked_image[center_x-rad:center_x+rad,center_y-rad,0] = 255
            masked_image[center_x-rad:center_x+rad,center_y+rad,0] = 255
            # Though centroid coordinates are sub-pixel values, they are
            # rounded here just for visualization
            start_coord = (round(center_x), round(center_y))
            end_coord = (round(init_x+centroid_x), round(init_y+centroid_y))
            # (y, x) indexing because numpy follows row, col indexing
            masked_image[round(start_coord[1]), round(start_coord[0]), 1] = 255
            # (x, y) is expected by cv2 for pixel coordinates
            masked_image = cv2.arrowedLine(masked_image, start_coord, end_coord,
                arrow_color, thickness, tipLength=0.3)
        return masked_image