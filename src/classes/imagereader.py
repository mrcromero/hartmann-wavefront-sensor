import sys
import cv2
import math
import numpy as np
import pandas as pd
from collections import Counter

# setting path
sys.path.append('./')

from .grid import Grid
from .blob import Blob

class ImageReader:
    image = None
    center_x = None
    center_y = None
    grid = None

    # The way the init works is subject to change depending on how image
    # streaming works
    # Regardless, would like to have an optional 'path' variable for testing
    # single images
    # Default values:
    def __init__(self, path):
        self.image = cv2.imread(path)
        self.center_x = len(self.image[0])//2
        self.center_y = len(self.image)//2
        self.centroid_coarse_grid()
        self.centroid_fine_grid()

    def centroid_coarse_grid(self):
        bw = cv2.cvtColor(self.image, cv2.COLOR_BGR2GRAY)

        # Threshold the image. This uses Otsu's thresholding method
        thresh = cv2.threshold(bw, 0, 255, cv2.THRESH_OTSU)[1]

        # Automate smoothing so we get an apporpriate number of components
        num_labels = 1000
        stel_size = 3
        while num_labels > 150:
            # Smooth edges
            kernel = cv2.getStructuringElement(cv2.MORPH_ELLIPSE,
                (stel_size,stel_size))
            opened = cv2.morphologyEx(thresh, cv2.MORPH_OPEN, kernel)

            # Detect connected components
            output = cv2.connectedComponentsWithStats(
                opened, 4, cv2.CV_32S)
            (num_labels, labels, stats, centroids) = output
            stel_size += num_labels//100

        
        # Automatically get the number of expected labels in the grid
        x_intervals = list(range(0, len(self.image[0])+50, 50))
        y_intervals = list(range(0, len(self.image)+50, 50))

        # Bin the centroids
        centroids_x = pd.cut(centroids[:, 0],
            bins=x_intervals, labels=x_intervals[:-1])
        centroids_y = pd.cut(centroids[:, 1],
            bins=y_intervals, labels=y_intervals[:-1])
        
        # Count the bin occurences
        cY_counts = Counter(centroids_y).values()
        cX_counts = Counter(centroids_x).values()
        # Find the most common counts, this is the size of our grid
        grid_x = Counter(cX_counts).most_common(1)[0][0]
        grid_y = Counter(cY_counts).most_common(1)[0][0]

        # Filter small components automatically
        area_factor = 0.01
        coarse_num_labels = num_labels
        max_area = max(stats[1:, cv2.CC_STAT_AREA])
        num_grid_elements = grid_x * grid_y
        final_centroids = []
        while (coarse_num_labels > num_grid_elements):
            final_centroids = []
            mask = bw.copy()
            mask[::] = 0
            labeled_mask = self.image.copy()
            coarse_num_labels = 0
            for i in range(1, num_labels):
                x = stats[i, cv2.CC_STAT_LEFT]
                y = stats[i, cv2.CC_STAT_TOP]
                w = stats[i, cv2.CC_STAT_WIDTH]
                h = stats[i, cv2.CC_STAT_HEIGHT]
                area = stats[i, cv2.CC_STAT_AREA]
                
                # filter small components depending on a percentage of the
                # max area
                if area > (max_area*area_factor):
                    coarse_num_labels += 1
                    component_mask = (labels == i).astype("uint8") * 255
                    mask = cv2.bitwise_or(mask, component_mask)
                
                    (cX, cY) = centroids[i]
                    cv2.rectangle(labeled_mask, 
                            (x, y), (x + w, y + h), (0, 255, 0), 3)
                    cv2.circle(labeled_mask, 
                            (int(cX), int(cY)), 4, (0, 0, 255), -1)
                    final_centroids.append([cX, cY])
            area_factor+=((coarse_num_labels-100)//10) * 0.01
        cv2.imshow('coarse components', mask)
        cv2.waitKey()
        cv2.imshow('coarse labeled components', labeled_mask)
        cv2.waitKey()
        cv2.destroyAllWindows()

    def centroid_fine_grid(self):
        return

    # Returns the grid created by the image. Creates the grid if specific
    # center coordinates are given or if the grid doesn't exist yet
    def get_grid(self, x=None, y=None):
        if self.grid != None:
            if x != None or y != None:
                self.center_x = x
                self.center_y = y
            else:
                return self.grid
        # Calibrate to the centroid of the center grid
        initial_x_start = self.center_x - (self.blob_size//2)
        initial_y_start = self.center_y - (self.blob_size//2)
        initial_blob = self.image[initial_y_start:initial_y_start+self.blob_size,
                                    initial_x_start:initial_x_start+self.blob_size]
        calibration_blob = Blob(initial_blob)
        self.center_x = round(calibration_blob.find_centroid().x) + initial_x_start
        self.center_y = round(calibration_blob.find_centroid().y) + initial_y_start
        
        # Calculate grid using center_x and center_y and place in grid
        edge_dist = math.ceil((self.grid_size/2) * self.blob_size)-1
        x_edges = [(self.center_x-edge_dist) + (self.blob_size*i) for i in range(self.grid_size+1)]
        y_edges = [(self.center_y-edge_dist) + (self.blob_size*i) for i in range(self.grid_size+1)]


        blob_array = []
        for i in range(self.grid_size):
            blob_array.append([])
            for j in range(self.grid_size):
                start_x = x_edges[j]
                start_y = y_edges[i]
                end_x = x_edges[j+1]
                end_y = y_edges[i+1]
                blob_mat = self.image[start_y:end_y, start_x:end_x]
                blob_array[i].append(Blob(blob_mat))

        grid = Grid(blob_array)
        self.grid = grid
        return grid

    # Grid updates according to changes in x and y
    def update_grid(self, delta_x, delta_y):
        length_to_edge = math.ceil((self.grid_size/2) * self.blob_size)
        new_x = self.center_x + delta_x
        new_y = self.center_y + delta_y
        if (new_x-length_to_edge < 0 or
            new_x+length_to_edge > len(self.image)-1 or
            new_y-length_to_edge < 0 or
            new_y+length_to_edge > len(self.image)-1):
            return self.get_grid()
        return self.get_grid(new_x, new_y)