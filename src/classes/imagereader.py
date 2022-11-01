from email.mime import image
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
    grid_len = 0
    grid_width = 0
    blob_size = 0
    blobs = []
    centers = []
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
        self.fit_grid()

    def centroid_coarse_grid(self):
        # Threshold the image. This uses Otsu's thresholding method
        bw = cv2.cvtColor(self.image, cv2.COLOR_BGR2GRAY)
        thresh = cv2.threshold(bw, 0, 255, cv2.THRESH_OTSU)[1]

        cv2.imshow('threshold', thresh)
        cv2.waitKey()

        # Automate smoothing so we get an apporpriate number of components
        num_labels = len(self.image)*len(self.image[0])
        prev_num_labels = num_labels*2
        stel_size = 3
        stats = None
        while num_labels < prev_num_labels:
            prev_num_labels = num_labels
            # Smooth edges
            kernel = cv2.getStructuringElement(cv2.MORPH_ELLIPSE,
                (stel_size,stel_size))
            opened = cv2.morphologyEx(thresh, cv2.MORPH_OPEN, kernel)
            # Detect connected components
            output = cv2.connectedComponentsWithStats(
                opened, 4, cv2.CV_32S)
            (num_labels, labels, stats, centroids) = output
            stel_size += num_labels//100
        
        cv2.imshow('smoothed', opened)
        cv2.waitKey()

        # Filter small components automatically
        area_factor = 0.2
        average_area = np.mean(stats[1:, cv2.CC_STAT_AREA])
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
            if area > (average_area*area_factor):
                coarse_num_labels += 1
                component_mask = (labels == i).astype("uint8") * 255
                mask = cv2.bitwise_or(mask, component_mask)
            
                (cX, cY) = centroids[i]
                cv2.rectangle(labeled_mask, 
                        (x, y), (x + w, y + h), (0, 255, 0), 3)
                cv2.circle(labeled_mask, 
                        (int(cX), int(cY)), 4, (0, 0, 255), -1)
                final_centroids.append([cX, cY])
        area_factor+= 0.01


        self.centers = final_centroids

        # Display found and labeled components
        cv2.imshow('coarse components', mask)
        cv2.waitKey()
        cv2.imshow('coarse labeled components', labeled_mask)
        cv2.waitKey()
        cv2.destroyAllWindows()

    def centroid_fine_grid(self):
        bw = cv2.cvtColor(self.image, cv2.COLOR_BGR2GRAY)
        
        # Estimate the radius of the blobs
        norms = []
        for start in self.centers:
            min_dist = None
            for end in self.centers:
                dist = np.linalg.norm([end[0]-start[0], end[1]-start[1]])
                if (start != end) and (min_dist == None or dist < min_dist):
                    min_dist = dist
            norms.append(min_dist)
        radius = np.average(norms)//2
        self.blob_size = int(radius*2)
        
        # Get the subimages for each blob
        labeled_mask = self.image.copy()
        new_centers = []
        for i in range(len(self.centers)):
            (cX, cY) = self.centers[i]
            x_start = int(int(cX)-radius)
            x_end = int(int(cX)+radius)
            y_start = int(int(cY)-radius)
            y_end = int(int(cY)+radius)
            # Make sure the blobs are within range for proper centroiding (not
            # clipped at the edge of the picture)
            if (x_start >= 0 and x_end < len(self.image[0]) and y_start >= 0 and y_end < len(self.image)):
                blob_mat = bw[y_start:y_end, x_start:x_end]
                cv2.rectangle(labeled_mask, 
                    (x_start, y_start), (x_end, y_end), (0, 255, 0), 3)
                # Convert the subimages to blobs to calculate centroids
                new_centers.append(self.centers[i])
                self.blobs.append(Blob(blob_mat, cX, cY))
        self.centers = new_centers
        cv2.imshow('fine labeled components', labeled_mask)
        cv2.waitKey()
    
    def fit_grid(self):
        bw = cv2.cvtColor(self.image, cv2.COLOR_BGR2GRAY)
        thresh = cv2.threshold(bw, 0, 255, cv2.THRESH_OTSU)[1]
        self.get_grid_size()

        # Create the kernel for cross-correlation. This is a perfect grid
        stel_size = self.blob_size
        kernel = cv2.getStructuringElement(cv2.MORPH_ELLIPSE,
            (stel_size,stel_size))
        grid_kernel = []
        row_kernel = []
        rows = []
        cols = []
        for i in range(self.grid_width):
            rows.append(kernel)
        row_kernel = np.hstack(tuple(rows))
        for i in range(self.grid_len):
            cols.append(row_kernel)
        grid_kernel = np.vstack(tuple(cols))
        cv2.imshow('kernel', grid_kernel*255)
        cv2.waitKey()      


        # Perform cross-correlation on all values and get the max's index
        radius = self.blob_size//2
        (grid_len_size, grid_width_size) = np.shape(grid_kernel)
        max = 0
        pos = 0
        grid = []
        for i in range(len(self.centers)):
            (cX, cY) = self.centers[i]
            x_start = int(cX-(grid_width_size//2 if self.grid_width%2 == 1 else (grid_width_size//2)-radius))
            y_start = int(cY-(grid_len_size//2 if self.grid_len%2 == 1 else (grid_len_size//2)-radius))
            x_end = int(cX+(grid_width_size//2 if self.grid_width%2 == 1 else (grid_width_size//2)+radius))
            y_end = int(cY+(grid_len_size//2 if self.grid_len%2 == 1 else (grid_len_size//2)+radius))
            if (x_start >= 0 and x_end < len(self.image[0]) and y_start >= 0 and y_end < len(self.image)):
                grid_image = thresh[y_start:y_end, x_start:x_end]
                cc_val = (grid_image*grid_kernel).sum()
                if cc_val > max:
                    max = cc_val
                    pos = i
                    grid = bw[y_start:y_end, x_start:x_end]
        
        labeled_mask = self.image.copy()
        (cX, cY) = self.centers[pos]
        x_start = int(cX-(grid_width_size//2 if self.grid_width%2 == 1 else (grid_width_size//2)-radius))
        y_start = int(cY-(grid_len_size//2 if self.grid_len%2 == 1 else (grid_len_size//2)-radius))
        cv2.rectangle(labeled_mask, (x_start, y_start),
            (x_start + grid_width_size, y_start + grid_len_size), (0, 255, 0), 3)
        cv2.imshow('fit grid', labeled_mask)
        cv2.waitKey()
        
        
        # Get new blobs after fitting the grid
        x_edges = [0 + (self.blob_size*i) for i in range(self.grid_width+1)]
        y_edges = [0 + (self.blob_size*i) for i in range(self.grid_len+1)]
        blob_array = []
        for i in range(self.grid_len):
            blob_array.append([])
            for j in range(self.grid_width):
                start_x = x_edges[j]
                start_y = y_edges[i]
                end_x = x_edges[j+1]
                end_y = y_edges[i+1]
                blob_mat = grid[start_y:end_y, start_x:end_x]
                blob_array[i].append(Blob(blob_mat))
        self.grid = Grid(blob_array)
    
    def get_grid_size(self):
        # Grid size values are assumed as 3x3 for now. Maybe there will be some way
        # to determine them later?
        self.grid_len = 3
        self.grid_width = 3