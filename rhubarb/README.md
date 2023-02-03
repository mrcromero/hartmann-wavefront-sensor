# AHWS Raspberry Pi Documentation

## By: Eric Torres

### Last updated: 31 Jan. 2023

<hr>
<a id="Contents"></a>

## Table of Contents

<ul>
    <li><a href="#Hardware"><b>Hardware</b></a></li>
    <ul>
        <li><a href="#OS"><b>OS</b></a></li>
        <li><a href="#Setup"><b>Setup</b></a></li>
        <ul>
            <li><a href="#initial"><b>Initial Setup</b></a></li>
            <li><a href="#ethernet"><b>Connecting via Ethernet</b></a></li>
            <li><a href="#vscode"><b>Setting up VS Code</b></a></li>
            <li><a href="#camera"><b>Enabling Camera (IMPORTANT)</b></a></li>
        </ul>
    </ul>
    <li><a href="#Software"><b>Software</b></a></li>
    <ul>
        <li><a href="#opencv"><b>OpenCV Troubleshooting</b></a></li>
        <li><a href="#Calibration"><b>Calibration</b></a></li>
    </ul>
</ul>
<hr>

<a id="Hardware"></a>

## Hardware:

<ul>
    <li>Rasperry Pi 4 Model B (4GB)</li>
    <li>ArduCam HQ Camera 12MP</li>
    <li>Display (optional but highly recommended. can use a plug-in one or connect to an external monitor)</li>
</ul>

<a id="OS"></a>

### OS:

This system uses the latest version of Debian Bullseye. Note that this prevents you from using any of the `raspistill` (or "legacy stack") family of commands, and you must instead use `libcamera`-based commands.

<a id="Setup"></a>

### Setup:

<a id="initial"></a>

#### Initial Setup

Initial set-up is pretty self-guided. Connect your Pi to power, plug in the display, and insert the SD Card with NOOBS (new, out of box software) on the underside of the Pi. Turn it on and follow the instructions on the screen. Official tutorial <a href="https://www.raspberrypi.com/documentation/computers/getting-started.html">here</a> (might be handy to plug in a USB mouse and keyboard) and many tutorials on Youtube.

(Hint: setting username and password as "pi" or something simple can make it easy to sign in, but just make sure nobody has access to your machine)

I proceeded with the "Update Software" step, but it can be skipped if you'd like (might take 10-15 minutes).

I changed the display to be horizontal so it would look better. You can do this by clicking the Pi symbol at the top left > Preferences > Screen Configuration > Right Click the rectangle that says HDMI-1 > Orientation > Right or Left > Apply > Yes

<a id="ethernet"></a>

<h4>Connecting via Ethernet</h4>

Not much is needed for developing on the raspberry pi; with a keyboard, mouse, and display you should be all good. However, if you want to connect it to your computer for easier programming (e.g using VS Code), you can connect it via ethernet.

<ol>
    <li>Enable SSH in the Pi Configuration Menu</li>
    <ul>
        <li>Click the Raspberry Pi Logo on the top left corner of the screen, then > Preferences > Raspberry Pi Configuration. Go to the "Interfaces" tab and enable "SSH", then click OK</li>
    </ul>
    <li>Edit the <tt>/etc/dhcpcd.conf</tt> file on the Pi. Full tutorial can be found <a href="https://www.zagrosrobotics.com/shop/custom.aspx?recid=84">here</a>, but the directions below should work just fine (and not mess up your Pi's connectivity).</li>
    <ul>
        <li>In the terminal, type <tt>sudo nano /etc/dhcpcd.conf</tt></li>
        <li>Add the following lines at the top of the file:<br>
            <code>interface eth0<br>static ip_address=192.168.4.1</code> (can be any number of your choosing, but make sure you don't set your PC's IP to that same number)
        </li>
        <li>Press CTRL + O, then ENTER to save. Then press CTRL + X to exit.</li>
        <li>You may need to reboot your Pi (<tt>sudo reboot</tt>)</li>
    </ul><br>
    <li>Change your Ethernet adapter settings on your computer. The following should be the minimum required steps for a Windows computer.</li><br>
    <ul>
        <li>From the search bar, search "Network Connections" and click "View Network Connections" in the Control Panel. Right click on your Ethernet Adapter and click <b>Properties</b><br><img src="https://www.circuitbasics.com/wp-content/uploads/2015/12/How-to-Connect-your-Raspberry-Pi-Directly-to-your-Laptop-or-Desktop-with-an-Ethernet-Cable-Network-Connections.png"></li><br>
        <li>Next, scroll until you see the IPv4 option, and double click it. (<b>Note:</b> you may need to disable IPv6 for this adapter in order for this to work! Try it if you have connection issues)<br><img src="https://www.circuitbasics.com/wp-content/uploads/2015/12/How-to-Connect-your-Raspberry-Pi-Directly-to-your-Laptop-or-Desktop-with-an-Ethernet-Cable-Internet-Protocol-Version-4-Properties.png"></li><br>
        <li>That will bring up the following menu, where you should input the following selections: (<b>doesn't match the image!!!</b>)</li>
        <ul>
            <li>Use the following IP Address:</li>
            <ul>
                <li>IP Address: (enter an address of the style 192.168.4.X, where X is any number between 0 and 255, and NOT the number you used for the Pi)</li>
                <li>Subnet mask: Should populate automatically, but for the IP we're using, it should be 255.255.255.0</li>
                <li>Default Gateway: Leave blank.</li>
            </ul>
            <li>Use the following DNS server addresses:</li>
            <ul>
                <li>Preferred DNS server: Insert the same IP as used above</li>
                <li>Alternate DNS server: leave blank</li>
            </ul>
        </ul><br>
        Image for reference:<br><img src="https://www.circuitbasics.com/wp-content/uploads/2015/12/How-to-Connect-your-Raspberry-Pi-Directly-to-your-Laptop-or-Desktop-with-an-Ethernet-Cable-Internet-Protocol-Version-4-Properties-IP-ADDRESS-ASSIGNED.png">
    </ul>
</ol>

To test it, do the following:

<ol>
    <li>Open the terminal on your computer</li>
    <li>Type <tt>ssh pi@192.168.4.1</tt> (or whatever IP you set in the Pi's config file).</li>
    <li>Type yes to add the fingerprint to your computer's known hosts, then type the Pi's password to log in</li>
</ol>

If it doesn't work, Google is your friend! You may need to edit the `known_hosts` file in your \<user\>/.ssh/ directory



Now your Pi and computer should be able to communicate via Ethernet! Ensure that your Pi is still connected to the internet. The way we have set it up may not allow for Internet to pass from your computer to your Pi. To do this, follow the steps <a href="">here</a>, which may require you to change the IP of your computer's Ethernet adapter (not a big problem, you will just need to edit your Pi's `/etc/dhcpcd.conf` file again to make sure you're on the same subnet)

(Note on subnets: To get the address for the network device, the IP Address is bit-wise OR'd with the subnet mask, so you get any numbers where the subnet mask is 1. For the host device, aka the Pi, you get anything where the subnet mask is 0.)

<a id="vscode"></a>

#### Setting up VS Code

There should be little to do here, and you can follow the steps in this <a href="https://singleboardblog.com/coding-on-raspberry-pi-remotely-with-vscode/">guide</a>. All you need to do when you open VSCode is press Ctrl + Shift + P and type "Connect to Remote Host". From there, click "Add new SSH Host", select a config file ("likely C://Users/<user/.etc") input the following lines:

```
Host <name you want it to show>
  HostName <IP of your Pi, the one you set in dhcpcd.conf file>
  User <username you chose for your Pi, e.g. "pi">
```

Then, select Linux as the OS, type in your Pi's password, and you should be set!



<a id="camera"></a>

#### Enabling Camera (IMPORTANT)

The camera should be fairly plug and play, but for some reason the Pi can sometimes have issues detecting the HQ Camera (IMX477). So, to fully ensure its operation, do the following:

<ol>
    <li><tt>sudo nano /boot/config.txt</tt></li>
    <li>Scroll down until you see <tt>camera_auto_detect=1</tt> and type a "#" in front to comment it out.</li>
    <li>Press Enter to type <tt>dtoverlay=imx477</tt> on the following line</li>
    <li>Type CTRL + O, ENTER to save and CTRL + X to exit</li>
    <li>You will need to reboot for changes to take effect (<tt>sudo reboot</tt>)</li>
</ol>
To test it, try running `libcamera-hello` or `libcamera-still -t 0`, which will open an infinite preview window of the camera (you will need to close out with your mouse). Otherwise, search commands on Google to find attached cameras (such as `dmesg | grep imx477` or `v4l2-ctl --list-formats` or running python live and creating a picamera2 object (lists cameras upon creation, or print object.sensor_modes). test

<a id="Software"></a>

## Software:

In order to use Python scripts that can run the new camera stack, we use the <a href="https://github.com/raspberrypi/picamera2">picamera2</a> library. General documentation for the library can be found <a href="https://datasheets.raspberrypi.com/camera/picamera2-manual.pdf">here</a>.

In software requirements put opencv-python version 4.6.0.66 or before

<a id="opencv"></a>

#### OPENCV TROUBLES???

If opencv isn't installing correctly, here are some tips that should help (especially 1-5):

1. `sudo apt install cmake`
2. ``sudo apt install libatlas-base-dev` (can look for other dependencies <a href="https://stackoverflow.com/a/53402396">here</a>, make sure you have matplotlib and numpy installed)
3. `pip3 install --upgrade pip setuptools wheel` (and trying to install again)
4. `pip3 install opencv-python==4.6.0.66 `(or earlier versions should work, but apparently 4.7.0.68 is the devil!)
5. `pip install -U numpy` (if you get an error like "numpy.core.multiarray failed to import")
6. using an older version of pip (like `pip3 install pip==21.3.1) (I haven't verified this)
7. `sudo apt install python3-opencv` (I ran this after I had opencv and it downloaded stuff but it never changed my opencv version... so I'm not sure this even works)

If all this stuff doesn't work... Good luck and may Google be ever in your favor!

\* Insert stuff about the stack setup here *

<a id="Calibration"></a>

### Calibration:

``` 
Note: currently going to explain how the script works, in the future we'll change it to explain that it runs on startup and how to re-run the script
```

This program performs the following primary actions:

<ul>
    <li>Capture raw images from camera sensor</li>
    <li>Unpack and debayer images into grayscale</li>
    <li>Find max saturation and adjust Exposure Time and Gain appropriately</li>
    <li>Display max saturation value to display via GUI</li>
</ul>
Images are taken at full resolution (3040 x 4056) pixels using the libcamera2 Python package. After the camera is configured to use the raw stream and the camera is started, the program enters a while loop to calibrate the sensor. In the loop, the first three actions in the list above are performed.

<h4>Capture Raw Images</h4>

Images are captured and temporarily stored in an array with `picam2.capture_array("raw")`. The argument to this function specifies which camera stream to use (other options are "main" and "lores").

<h4>Unpack and debayer image into grayscale</h4>

This takes a couple of steps. The IMX477 camera stores raw images with in the SRGGB12_CSI2P format, which means the data is stored in the RGGB pattern, every pixel is represented in 12 bits, and bits are packed together ("CSI2P", unpacked format is possible*). Thus, 2 pixels are stored in 3 consecutive bytes in the array, as:

AAAAAAAA BBBBBBB BBBBAAAA (<a href="https://www.strollswithmydog.com/open-raspberry-pi-high-quality-camera-raw/">source</a>)

These are unpacked in a short loop in the code that shifts bits and stores them in a new, uint16 (unsigned 16-bit integer) numpy array and forms a Bayered image. To debayer the image, we use OpenCV's `cvtColor` command to change colorspace and debayer it into grayscale, with `cv2.cvtColor(<img_arr_name>, cv2.COLOR_BAYER_BG2GRAY)`. Using BG2GRAY assumes BGGR bayer pattern (which may be wrong actually but you can use RG2GRAY to double check)



*(You can also use an unpacked format in 2 ways: when creating the configuration, add a parameter "format" = "SRGGB12" leaving out the CSI2P part, or after making the configuration type `config["raw"]["format"] = "SRGGB12"`). However, this still uses a uint8 array to store the values, they are just spread out into more bytes, which would require a different method to unpack. If I had to guess, it's probably something like AAAAAAAA 0000AAAA BBBBBBBB 0000BBBB, but I'd have to look into it or test it myself.



#### Find Max Saturation and Adjust Exposure/Gain

Once the debayered, grayscale array is obtained, the maximum saturation can easily be found by using `np.amax(<array>)`.

If the max value is greater than 80% of max saturation, exposure time and gain are decreased by the same amount, a fixed percentage set earlier in the code by the `pct` variable.

If the max value is less than 40% of max saturation, exposure time and gain are increased by the same amount, also by `pct` percent.



#### Display Max Saturation via GUI

To display the information in a user-friendly way, we use tkinter to make a simple GUI. After setting size parameters with `rowconfigure` and `columnconfigure`, we use a tkinter StringVar() that we can update throughout the code and simultaneously update the display. When creating a tkinter label, we use `textvariable=<varname>` to enable this.

More importantly, the use of a GUI while reading sensor data requires the use of multithreading.

Once the max saturation falls within the desired range of 40%-80%, the program will pause and the GUI will be left running. In order to end the program, you must manually close the GUI window with your mouse (future work: have loop close on its own).



### Useful Camera Commands (picam2.____)

<ul>
    <li><tt>sensor_modes</tt></li>
    <li><tt>capture_array()</tt></li>
    <li></li>
</ul>
