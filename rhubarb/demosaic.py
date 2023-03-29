# demosaic.py

import numpy as np
from picamera2 import Picamera2, Preview
import cv2
import time
from PIL import Image
import sys
import tkinter as tk
from tkinter import ttk
from datetime import datetime
import threading
import queue

# Set path
import pathlib
sys.path.append('/'.join(str(pathlib.Path(__file__).parent.resolve()).split('/')[:-1]))

from src.classes.imagereader import ImageReader
from src.classes.zernikesolver import ZernikeSolver


"""
Name: start_cam()
Description: all-encompassing function that creates tkinter GUI, Picamera2 camera, calibrates camera, and runs files to compute Zernike coefficients
Inputs: None
Outputs: None
"""
def start_cam():  # can just be moved into start_cam() i think

    # makes display window
    root = tk.Tk()
    root.rowconfigure(0, minsize=200, weight=1)
    root.columnconfigure(0, minsize=200, weight=1)
    txt = tk.StringVar()

    controls = {}  # supposedly changed by calibrate_cam()

    coeffs = [None] * 15
    camera = create_cam()
    update_queue = queue.Queue()  ### NOTE: may want to consider emptying queue after use
    img = np.array([])  # supposedly changed by calibrate_cam()

    task = threading.Thread(target=calibrate_cam, daemon=True, args=(camera, update_queue, controls, img))  # create and pass through update queue
    task.start()
    while task.is_alive():  # do this until calibration is complete
        root.after(100, update_txt, txt, update_queue,root) # pass through root, update every 100ms

    other_stuff(img)

    root.mainloop()  # does it even get to here??  # should add something to destroy window after a while
    sys.exit()


"""
Name: read_cam()
Description: Takes a raw 16-bit image with camera sensor and returns image as 16-bit numpy array
Inputs:
- camera; Picamera2 object representing camera in use
Outputs:
- im; numpy array of unsigned 16-bit integers representing image taken
"""
def read_cam(camera):  # could pass in the "im" array so we don't have to create and destroy object repeatedly
    raw = camera.capture_array("raw")
    raw = raw[:3040, :6084]
    raw16 = raw.astype(np.uint16)  # raw array is 8-bit by default. must use 16-bit int if we want to use image as 16-bit

    im = np.zeros((3040, 4056), dtype=np.uint16)  # this doesn't have to be in loop, can be passed into function

    for byte in range(2):
        # SRGGB12_CSI2P format bit unpacking
        im[:, byte::2] = ( (raw16[:, byte::3] << 4) | ((raw16[:, 2::3] >> (byte * 4)) & 0b1111) )  # unpacks bytes of image into respective pixels

    im = im * 16  # converting from 12-bit to 16-bit values (otherwise would appear too dark)

    return im  # returns raw, 16-bit image


"""
Name: other_stuff()  (Marco's code)
Description: runs additional code Marco wrote
Inputs:
- img; numpy array representing image to be analyzed
Outputs: None
"""
def other_stuff(img):
    c = [None] * 15
    reader = ImageReader(imm_arr=img, previews = False)   ### NOTE: img must be 8-bit grayscale image
    grid = reader.grid
    coeffs = ZernikeSolver(grid).solve()
    # By assigning the values to the c array, we can acess it in the start_cam
    # function. We would also be able to add it to the UI
    for i in range(len(c)):
        c[i] = int(coeffs[i])



"""
Name: imgRaw2Gray()
Description: converts Bayer image to grayscale
Inputs: raw; numpy array representing Bayer image
Outputs: grayscale version of input array
"""
def imgRaw2Gray(raw):
    return(cv2.cvtColor(raw, cv2.COLOR_BAYER_BG2GRAY))



"""
Name: update_display()
Description: Updates the value used in the Raspi Display showing Max Saturation and Iteration Count
Inptus:
- arrmax; max value of image pixel value, representing max saturation value
- update_queue; Queue object that holds values which will be used to update display in update_txt() function
- max_val; maximum value possible by camera resolution (e.g. for 16-bits, is 2^16)
- counter; iteration number the calibration step is currently on. has default of 0, can be removed entirely
Outputs: None
"""
def update_display(arrmax, update_queue, max_val, counter=0):  # don't really need counter. max_val could also be hardcoded
    update_queue.put(f"Max Saturation: {arrmax/max_val*100:.2f}%\nIteration: {counter}")



"""
Name: update_txt()
Description: Updates text variable used in tkinter GUI
Inputs:
- txt; text string variable that is displayed by GUI and is updated with next value to be displayed
- update_queue; Queue object containing next values to be displayed
Outputs: None
"""
def update_txt(txt, update_queue): #pass root as arg
    try:
        message = update_queue.get_nowait()
        txt.set(message)
        # update_queue.task_done()  # would this remove the task from the queue and prevent it from growing unnecessarily larger?
    except queue.Empty:
        pass


"""
Name: calibrate_cam()
Description: runs routine to calibrate camera and set controls
Inputs:
- camera;
- update_queue; queue object used for running multithreaded display content
- controls
Outputs:
- dictionary containing keys ExposureTime and AnalogueGain
"""
def calibrate_cam(camera, update_queue, controls):  # don't know what i/o i need
    
    max_val = 1 << 16
    max_iter = 100
    counter = 0
    pct = 0.15

    ct_list = ["ExposureTime", "AnalogueGain"]

    gray = None
    while True:
        
        # do the reading, conversion, and checking/adjusting controls in here
        raw = read_cam(camera)
        gray = imgRaw2Gray(raw)
        arrmax = np.amax(gray)
        update_display(arrmax, update_queue, max_val, counter)  # more so updates display values?

        metadata = camera.capture_metadata()
        exposure, gain = [metadata[c] for c in ct_list]  # note this is only meant to show 2 parameters, if ct_list is larger it will fail

        if (arrmax > (0.8 * max_val)):  # scene is too BRIGHT
            counter += 1
            exposure = int(np.floor((1 - pct) * exposure))
            gain = (1 - pct) * gain
            camera.set_controls({"ExposureTime": exposure, "AnalogueGain": gain})

        elif (arrmax < (0.4 * max_val)):  # scene is too DARK
            counter += 1
            exposure = int(np.floor((1 + pct) * exposure))
            gain = (1 + pct) * gain
            camera.set_controls({"ExposureTime": exposure, "AnalogueGain": gain})
        else:
            img = gray
            break
        
        # printing exposure time and gain without having to call metadata method again
        print(f"'ExposureTime': {exposure}, 'AnalogueGain': {gain}")
        controls = {"ExposureTime": exposure, "AnalogueGain": gain}  # i am praying this works and updates the actual dict i passed in



"""
Name: start_cam()
Description: makes a camera object and initalizes it with default parameters
Inputs: None
Outputs:
- picam2; Picamera2 object with initialized camera
"""
def create_cam():

    picam2 = Picamera2()

    exposure = 10000
    gain = 1.0

    config = picam2.create_still_configuration(raw={"size": picam2.sensor_resolution})
    picam2.configure(config)
    picam2.set_controls({"ExposureTime": exposure, "AnalogueGain": gain})

    picam2.start()
    time.sleep(2)

    return picam2


def not_used():
    # Hold the coefficients
    c = [None] * 15

    root = tk.Tk()
    root.rowconfigure(0, minsize=200, weight=1)
    root.columnconfigure(0, minsize=200, weight=1)
    txt = tk.StringVar()
    
    task = threading.Thread(target=read_cam, daemon=True, args=(txt, c, update_queue)) #create and pass through update queue
    task.start()
    root.after(100, update_txt, txt, update_queue,root) #pass through root
    root.mainloop()



    sys.exit()