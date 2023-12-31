# CS370 FA23 Term Project : Automatic Blinds

## People
 - Collin Conrad
 - Jared Traub
 - John Mulligan

This project implements a set of smart blinds that react to outdoor lighting
conditions, and indoor motion detection. This way the blinds can maximize
user-experience (allowing outside light in when a room is in use), and minimize
hvac energy usage (by blocking light and reducing incomming heat in the summer)

## Parts Used
 - Raspberry Pi
 - Webcam (sensor) : Used to detect motion
 - Light Dependent Resistor (Sensor) : Used to detect ouside lighting conditions

More than anything, this project is a proof of concept designed to prototype
this idea, and realistically, you'd want to replace some components with those
more subtible for mass production and reliability. Some of these changes could
include a more purpose-built actuactor, lower-power and efficient processor
(something like a esp8266 or other lower power wireless-capable microcontroller
would work well here), and a more power-efficient motion detection system (like
a pir sensor).

That being said, this project should still have enough to prove the feasability
of a device like this.

## Project Architecture

The project is split into a handfull of different "segments", with each running in
their own seperate process (courtesy of python's multiprocessing). Each communicates
via a queue with the Main process, which acts as a message bus and the primary state
machine for the entire project.

From there there are a handful of different "modules"

### HAL

The hardware abstraction layer allows us to abstract any hardware details away (e.g.
for simulation or porting), and write all the code in a more general way

### Motion Detection

This component uses opencv to track and notify the state machine if any motion is
detected on the webcam

### Web interface/Logging

This compoent runs a web-server, which will allow the user to control the blinds, as
well as view metrics such as how often they've been triggered, as well as potential
power savings they may have gotten


## Usage

1. Install all the requirments with pip (eg. `pip install -r requirments.txt`)

2. NOTE: for camera support also `pip install opencv-python`

3. `cd blinds`

4. `python3 main.py`


Because of the design, the camera and hardware support are locked behind
enviroment variables, which default to mock versions if they aren't enabled.

 - `USECAMERA` : Enable camera support (relies on opencv being installed)
 - `USESERIAL` : Enable the serial HAL module (relies on an arduino running
the provided .ino file being connected as `/dev/ttyUSB0`)

## Sources Used

https://pimylifeup.com/raspberry-pi-light-sensor/
https://www.circuitbasics.com/pairing-a-light-dependent-resistor-ldr-with-an-arduino-uno/
https://forum.arduino.cc/t/very-slow-rolling-average/665489/7
https://askubuntu.com/questions/1408365/wsl-how-do-i-set-the-group-for-a-tty-device
https://askubuntu.com/questions/112568/how-do-i-allow-a-non-default-user-to-use-serial-device-ttyusb0
https://unix.stackexchange.com/questions/14354/read-write-to-a-serial-port-without-root
https://www.cyberciti.biz/faq/find-out-linux-serial-ports-with-setserial/

https://learn.microsoft.com/en-us/windows/wsl/connect-usb#install-the-usbipd-win-project

https://medium.com/@abbessafa1998/motion-detection-techniques-with-code-on-opencv-18ed2c1acfaf
