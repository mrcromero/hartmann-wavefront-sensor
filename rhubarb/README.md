# AHWS Raspi Documentation

## By: Eric Torres

### Last updated: 31 Jan. 2023

<hr>

## <b>Table of Contents</b>

<ul>
    <li><a href="#Hardware"><b>Hardware</b></a></li>
    <ul>
        <li><a href="#OS"><b>OS</b></a></li>
        <li><a href="#Setup"><b>Setup</b></a></li>
    </ul>
    <li><a href="#Software"><b>Software</b></a></li>
    <ul>
        <li><b>Calibration</b></li>
    </ul>
</ul>



<a id="Hardware"></a>

## <b>Hardware:</b>

<ul>
    <li>Rasperry Pi 4 Model B (4GB)</li>
    <li>ArduCam HQ Camera 12MP</li>
    <li>Display (optional)</li>
</ul>

<a id="OS"></a>

### <b>OS:</b>

This system uses the latest version of Debian Bullseye. Note that this prevents you from using any of the `raspistill` (or "legacy stack") family of commands, and you must instead use `libcamera`-based commands.

<a id="Setup"></a>

### Setup:

Not much is needed for developing on the raspberry pi; with a keyboard, mouse, and display you should be all good. However, if you want to connect it to your computer for easier programming, you can connect it via ethernet.

<ol>
    <li>Edit the <tt>/etc/dhcpcd.conf</tt> file on the Pi. Full tutorial can be found <a href="https://www.zagrosrobotics.com/shop/custom.aspx?recid=84">here</a>, but the directions below should work just fine (and not mess up your Pi's connectivity).</li>
    <ul>
        <li>In the terminal, type <tt>sudo nano /etc/dhcpcd.conf</tt></li>
        <li>Add the following lines at the top of the file:<br>
            <code>interface eth0<br>static ip_address=192.168.4.1</code> (can be any number of your choosing)
        </li>
    </ul><br>
    <li>Change your Ethernet adapter settings on your computer. The following should be the minimum required steps for a Windows computer.</li><br>
    <ul>
        <li>From the search bar, search "Network Connections" and click "View Network Connections" in the Control Panel. Right click on your Ethernet Adapter and click <b>Properties</b><br><img src="https://www.circuitbasics.com/wp-content/uploads/2015/12/How-to-Connect-your-Raspberry-Pi-Directly-to-your-Laptop-or-Desktop-with-an-Ethernet-Cable-Network-Connections.png"></li><br>
        <li>Next, scroll until you see the IPv4 option, and double click it.<br><img src="https://www.circuitbasics.com/wp-content/uploads/2015/12/How-to-Connect-your-Raspberry-Pi-Directly-to-your-Laptop-or-Desktop-with-an-Ethernet-Cable-Internet-Protocol-Version-4-Properties.png"></li><br>
        <li>That will bring up the following menu, where you should input the following selections: (<b>doesn't match the image!!!</b>)</li>
        <ul>
            <li>Use the following IP Address:</li>
            <ul>
                <li>IP Address: (enter an address of the style 192.168.4.X, where X is any number between 0 and 255)</li>
                <li>Subnet mask: Should populate automatically, but for the IP we're using, it should be 255.255.255.0</li>
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

<a id="Software"></a>

### <b>Software:</b>

In order to use Python scripts that can run the new camera stack, we use the <a href="https://github.com/raspberrypi/picamera2">picamera2</a> library. General documentation for the library can be found <a href="https://datasheets.raspberrypi.com/camera/picamera2-manual.pdf">here</a>.

\* Insert stuff about the stack setup here *

### <b>Calibration:</b>

``` 
Note: currently going to explain how the script works, in the future we'll change it to explain that it runs on startup and how to re-run the script
```

