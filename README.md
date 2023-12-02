# CS370 FA23 Term Project

This project implements a set of smart blinds that react to outdoor lighting
conditions, and indoor motion detection. This way the blinds can maximize
user-experience (allowing outside light in when a room is in use), and minimize
hvac energy usage (by blocking light and reducing incomming heat in the summer)

This project is built with a...
	- Raspberry Pi
	- Light Dependent Resistor (LDR) : Light sensor
	- Webcam : Motion detection (with opencv)
	- SG90 servo : Actuator for blinds

More than anything, this project is a proof of concept designed to prototype
this idea, and realistically, you'd want to replace some components with those
more subtible for mass production and reliability. Some of these changes could
include a more purpose-built actuactor, lower-power and efficient processor
(something like a esp8266 or other lower power wireless-capable microcontroller
would work well here), and a more power-efficient motion detection system (like
a pir sensor).

That being said, this project should still have enough to prove the feasability
of a solution like this.
