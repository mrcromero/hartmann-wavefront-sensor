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
    grid_kernel = None
    grid_len = 0
    grid_width = 0
    grid_len_size = 0
    grid_width_size = 0
    aperture_rad = 0
    blob_size = 0
    radius = 0
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

    # Gets size of the grid. We are assuming this will be constant
    def get_grid_size(self):
        # Grid size values are assumed as 5x5
        self.grid_len = 5
        self.grid_width = 5

    # Gets the size of the aperture. We are assuming this will be constant
    def get_aperture_size(self):
        # Grid size is assumed to be 1000px, so radius is 500px
        self.aperture_rad = 500

    # Gets the radius size (distance between blobs)
    def get_radius_size(self):
        # Estimate the radius of the blobs
        # norms = []
        # for start in self.centers:
        #     min_dist = None
        #     for end in self.centers:
        #         dist = np.linalg.norm([end[0]-start[0], end[1]-start[1]])
        #         if (start != end) and (min_dist == None or dist < min_dist):
        #             min_dist = dist
        #     norms.append(min_dist)
        # self.radius = np.average(norms)//2
        self.radius = 172//2

    def smooth_image(self, thresh):
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
        return (labels, stats, centroids, num_labels)
    
    def filter_small_comps(self, bw, stats, centroids, labels, num_labels):
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

        # Display found and labeled components
        cv2.imshow('coarse components', mask)
        cv2.waitKey()
        cv2.imshow('coarse labeled components', labeled_mask)
        cv2.waitKey()
        cv2.destroyAllWindows()

        return mask, final_centroids

    def display_component_image(self):
        # Get the subimages for each blob
        labeled_mask = self.image.copy()
        new_centers = []
        for i in range(len(self.centers)):
            (cX, cY) = self.centers[i]
            x_start = int(int(cX)-self.radius)
            x_end = int(int(cX)+self.radius)
            y_start = int(int(cY)-self.radius)
            y_end = int(int(cY)+self.radius)
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

    # Sets the kernel for cross-correlation
    def set_kernel(self):
        # Create the kernel for cross-correlation. This is a perfect grid
        stel_size = int(self.radius*2)
        kernel = cv2.getStructuringElement(cv2.MORPH_ELLIPSE,
            (stel_size,stel_size))
        row_kernel = []
        rows = [kernel]*self.grid_width
        row_kernel = np.hstack(tuple(rows))
        cols = [row_kernel]*self.grid_len
        self.grid_kernel = np.vstack(tuple(cols))
        (self.grid_len_size, self.grid_width_size) = np.shape(self.grid_kernel)
        cv2.imshow('kernel', self.grid_kernel*255)
        cv2.waitKey()
    
    # Cycles through the found blobs and performs cross-correlation to find the
    # optimum spot for the grid
    #
    # returns: the position in the centers array for the optimum grid position
    def cross_correlation(self):
        bw = cv2.cvtColor(self.image, cv2.COLOR_BGR2GRAY)
        thresh = cv2.threshold(bw, 0, 255, cv2.THRESH_OTSU)[1]
        max_val = 0
        pos = 0
        for i in range(len(self.centers)):
            (cX, cY) = self.centers[i]
            x_start = int(cX-(self.grid_width_size//2 if self.grid_width%2 == 1 else (self.grid_width_size//2)-self.radius))
            y_start = int(cY-(self.grid_len_size//2 if self.grid_len%2 == 1 else (self.grid_len_size//2)-self.radius))
            x_end = int(cX+(self.grid_width_size//2 if self.grid_width%2 == 1 else (self.grid_width_size//2)+self.radius))
            y_end = int(cY+(self.grid_len_size//2 if self.grid_len%2 == 1 else (self.grid_len_size//2)+self.radius))
            # Check if the grid will be outside of the image
            if (x_start >= 0 and x_end < len(self.image[0]) and y_start >= 0 and y_end < len(self.image)):
                # Get the sub-grid and perform cross-correlation to check fit
                grid_image = thresh[y_start:y_end, x_start:x_end]
                cc_val = (grid_image*self.grid_kernel).sum()
                if cc_val > max_val:
                    max_val = cc_val
                    pos = i
        return pos

    # Gets the new Grid object based on the given grid
    #
    # args: grid -- the grid matrix
    #       y_shift -- the shift in the y-axis to normalize blob positions
    #       x_shift -- the shift in the x-axis to normalize blob positions
    #
    # returns: new Grid object
    def get_grid_object(self, grid, y_shift, x_shift):
        # Get new blobs after fitting the grid
        blob_size = int(self.radius*2)
        x_edges = [0 + (blob_size*i) for i in range(self.grid_width+1)]
        y_edges = [0 + (blob_size*i) for i in range(self.grid_len+1)]
        blob_array = []
        for i in range(self.grid_len):
            blob_array.append([])
            for j in range(self.grid_width):
                start_x = x_edges[j]
                start_y = y_edges[i]
                end_x = x_edges[j+1]
                end_y = y_edges[i+1]
                # These values are used for normalizing the positions of the
                # grid
                center_x = (((start_x+end_x)//2) + y_shift)/self.aperture_rad
                center_y = (((start_y+end_y)//2) + x_shift)/self.aperture_rad
                blob_mat = grid[start_y:end_y, start_x:end_x]
                blob_array[i].append(Blob(blob_mat, center_x, center_y))
        return Grid(blob_array)

    # Performs coarse grid automation -- finds possible blob locations
    def centroid_coarse_grid(self):
        # Threshold the image. This uses Otsu's thresholding method
        bw = cv2.cvtColor(self.image, cv2.COLOR_BGR2GRAY)
        thresh = cv2.threshold(bw, 0, 255, cv2.THRESH_OTSU)[1]
        cv2.imshow('threshold', thresh)
        cv2.waitKey()

        # Smooth the image
        (labels, stats, centroids, num_labels) = self.smooth_image(thresh)
        # Filter out small components
        self.centers = self.filter_small_comps(bw, stats, centroids, labels, num_labels)

    # Performs fine grid automation -- finds actual blob locations and sizes
    def centroid_fine_grid(self):
        # Get the radius of the blobs
        self.get_radius_size()

        self.display_component_image()

    # Performs grid fitting via cross-correlation of an "ideal" grid
    def fit_grid(self):
        bw = cv2.cvtColor(self.image, cv2.COLOR_BGR2GRAY)
        self.get_grid_size()

        # Create the kernel for cross-correlation. This is a perfect grid
        self.set_kernel()

        # Perform cross-correlation on all values and get the max's index
        pos = self.cross_correlation()
        # Get positions of final grid after cross correlation fitting
        (cX, cY) = self.centers[pos]
        x_start = int(cX-(self.grid_width_size//2 if self.grid_width%2 == 1 else (self.grid_width_size//2)-self.radius))
        y_start = int(cY-(self.grid_len_size//2 if self.grid_len%2 == 1 else (self.grid_len_size//2)-self.radius))
        x_end = int(cX+(self.grid_width_size//2 if self.grid_width%2 == 1 else (self.grid_width_size//2)+self.radius))
        y_end = int(cY+(self.grid_len_size//2 if self.grid_len%2 == 1 else (self.grid_len_size//2)+self.radius))
        grid = bw[y_start:y_end, x_start:x_end]
        
        # Just for showing the image
        labeled_mask = self.image.copy()
        (cX, cY) = self.centers[pos]
        x_start = int(cX-(self.grid_width_size//2 if self.grid_width%2 == 1 else (self.grid_width_size//2)-self.radius))
        y_start = int(cY-(self.grid_len_size//2 if self.grid_len%2 == 1 else (self.grid_len_size//2)-self.radius))
        cv2.rectangle(labeled_mask, (x_start, y_start),
            (x_start + self.grid_width_size, y_start + self.grid_len_size), (0, 255, 0), 3)
        cv2.imshow('fit grid', labeled_mask)
        cv2.waitKey()

        self.get_aperture_size()

        new_grid = self.get_grid_object(grid, y_start-cY, x_start-cX)
        self.grid = new_grid