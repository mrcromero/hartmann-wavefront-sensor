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

# Set path
import pathlib
sys.path.append('/'.join(str(pathlib.Path(__file__).parent.resolve()).split('/')[:-1]))

from src.classes.imagereader import ImageReader
from src.classes.zernikesolver import ZernikeSolver


def read_cam(txt, c):
    picam2 = Picamera2()

    max_val = 1 << 16
    exposure = 10000
    gain = 1.0
    date = datetime.today().strftime('%m_%d_%Y')

    max_iter = 100
    pct = .15  # percent increase/decrease of exposure time and gain
    ct_list = ["ExposureTime", "AnalogueGain"]
    counter = 0


    config = picam2.create_still_configuration(raw={"size": picam2.sensor_resolution})
    picam2.configure(config)
    picam2.set_controls({"ExposureTime": exposure, "AnalogueGain": gain})

    picam2.start()
    time.sleep(2)

    gray = None
    while True:

        if (counter > max_iter):
            break

        # all the camera commands + processing, need to time it
        raw = picam2.capture_array("raw")  # i could get fancy and do multiple captures, doubt it's necessary
        raw = raw[:3040, :6084]
        raw16 = raw.astype(np.uint16)  # raw array is 8 bit, convert to 16 bit. don't know why it's necessary but it is!...

        im = np.zeros((3040, 4056), dtype=np.uint16)  # this doesn't have to be in loop

        for byte in range(2):
            im[:, byte::2] = ( (raw16[:, byte::3] << 4) | ((raw16[:, 2::3] >> (byte * 4)) & 0b1111) )

        im16 = im * 16
        im = im16

        # rgb = cv2.cvtColor(im, cv2.COLOR_BAYER_BG2RGB)
        gray = cv2.cvtColor(im, cv2.COLOR_BAYER_BG2GRAY)

        arrmax = np.amax(gray)
        txt.set(f"Max Saturation: {arrmax/max_val*100:.2f}%\nIteration: {counter}")
        # print(f'arrmax = {arrmax}')
        # print(f"iter = {counter}")

        if (arrmax > (0.8 * max_val)):  # scene is too BRIGHT
            counter += 1
            exposure = int(np.floor((1 - pct) * exposure))
            gain = (1 - pct) * gain
            picam2.set_controls({"ExposureTime": exposure, "AnalogueGain": gain})
            metadata = picam2.capture_metadata()
            controls = {c: metadata[c] for c in ct_list}
            print(controls)

        elif (arrmax < (0.4 * max_val)):  # scene is too DARK
            counter += 1
            exposure = int(np.floor((1 + pct) * exposure))
            gain = (1 + pct) * gain
            picam2.set_controls({"ExposureTime": exposure, "AnalogueGain": gain})
            metadata = picam2.capture_metadata()
            controls = {c: metadata[c] for c in ct_list}
            print(controls)

        else:  # it is within range and can exit
            # exit = 1  # redundant
            break
    # Perform wavefront reconstruction
    reader = ImageReader(imm_arr=gray, previews=False)
    grid = reader.grid
    coeffs = ZernikeSolver(grid).solve()
    # By assigning the values to the c array, we can acess it in the start_cam
    # function. We would also be able to add it to the UI
    for i in range(len(c)):
        c[i] = int(coeffs[i])

def start_cam():
    # Hold the coefficients
    c = [None] * 15

    root = tk.Tk()
    root.rowconfigure(0, minsize=200, weight=1)
    root.columnconfigure(0, minsize=200, weight=1)
    txt = tk.StringVar()
    lbl = tk.Label(root, textvariable=txt).grid(row=0, column=0)

    task = threading.Thread(target=read_cam, daemon=True, args=(txt, c))
    task.start()
    task.join()
    root.mainloop()


    sys.exit()

def not_sure():
    raw = picam2.capture_array("raw")  # i could get fancy and do multiple captures, doubt it's necessary
    raw = raw[:3040, :6084]
    # print(raw.shape)
    raw16 = raw.astype(np.uint16)  # raw array is 8 bit, convert to 16 bit. don't think it's necessary...

    im = np.zeros((3040, 4056), dtype=np.uint16)  # this doesn't have to be in loop

    for byte in range(2):
        im[:, byte::2] = ( (raw16[:, byte::3] << 4) | ((raw16[:, 2::3] >> (byte * 4)) & 0b1111) )

    # unpacked12b = Image.fromarray(im)
    # unpacked12b.save(f"{date}_unpacked12b.png")
    # im8 = im.astype(np.uint8)
    im16 = im * 16
    im = im16
    # unpacked16b = Image.fromarray(im)
    # unpacked16b.save(f"{date}_unpacked16b.png")

    rgb = cv2.cvtColor(im, cv2.COLOR_BAYER_BG2RGB)
    # rgbim = Image.fromarray(rgb, "RGB")
    # rgbim.save(f"{date}_rgb.png")
    # rgb16 = rgb * 16
    # rgb8 = rgb.astype(np.uint8)
    gray = cv2.cvtColor(im, cv2.COLOR_BAYER_BG2GRAY)
    # grayim = Image.fromarray(gray)
    # grayim.save(f"{date}_gray.png")
    # gray8 = gray.astype(np.uint8)
    # print(f'gray shape = {gray.shape}')
    # print(f'rgb shape = {rgb.shape}')
    # print(type(rgb))

    # img = Image.fromarray(rgb16, 'RGB')
    # img = Image.fromarray(gray8)
    # img = Image.fromarray(im)
    # img.show()

    # cv2.imshow("yes", im16)
    # cv2.waitKey(0)
    # cv2.destroyAllWindows()


    # gain shouldn't go below 1?
    # exposure, find camera min value?
    # auto-exposure?
    # auto ISP

    # arrmax = np.amax(gray)
    # if (arrmax > (0.8 * max_val)):
    #     counter += 1
    #     exposure = int(np.floor((1 - pct) * exposure))
    #     gain = np.floor((1 - pct) * gain)
    #     picam2.set_controls({"ExposureTime": exposure, "AnalogueGain": gain})
    #     metadata = picam2.capture_metadata()
    #     controls = {c: metadata[c] for c in ["ExposureTime", "AnalogueGain", "ColourGains"]}
    #     print(controls)
    # elif (arrmax < (0.4 * max_val)):
    #     counter += 1
    #     exposure = int(np.floor((1 + pct) * exposure))
    #     gain = np.floor((1 + pct) * gain)
    #     picam2.set_controls({"ExposureTime": exposure, "AnalogueGain": gain})
    #     metadata = picam2.capture_metadata()
    #     controls = {c: metadata[c] for c in ["ExposureTime", "AnalogueGain", "ColourGains"]}
    #     print(controls)
    # else:  # it is within range and can exit
    #     exit = 1  # redundant
    #     # break
