# CS370 Final Project : Automatic Blinds

## People
 - Collin Conrad
 - Jared Traub
 - John Mulligan

## Description

Our goal is to use a raspberry pi, webcam, and light sensor to build a set of smart blinds that
react to inside motion and outside lighting conditions to maximize their utiltiy, as well as save energy costs

This is done by opening the blinds when it is light outside and motion is detected inside, and closing them
when it is dark outside or there is no motion. This allows them to prevent sunlight from comming in and heating up
an otherwise empty room, saving AC costs.

## Parts Used
 - Raspberry Pi
 - Webcam (sensor) : Used to detect motion
 - Light Dependent Resistor (Sensor) : Used to detect ouside lighting conditions

## Project Archetecture

The project is split up into a two seperate parts

 - Blinds Program
 	- Actually interfaces with the hardware, and executes the logic for the motion dectection
 - Gui
 	- Allows you to view and change the current state of the program
