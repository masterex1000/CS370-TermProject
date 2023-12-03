# This is the hardware abstraction layer for using an arduino connected to the pi via serial.
# This was the simplest way i could quickly throw this stuff together lol

import serial

SERIAL_PORT = '/dev/ttyUSB0'

class BlindHal:
    """A serial-based hal for the project"""

    lightState = False

    def __init__(self):
        self.port = serial.Serial(SERIAL_PORT)
    
    def makeSerialAvail(self):
        if(not self.port.is_open):
            self.port = serial.Serial(SERIAL_PORT)

    def isLight(self) -> bool:
        self.makeSerialAvail()

        while(self.port.in_waiting > 0):
            b = self.port.read()

            if(b == b'l'):
                self.lightState = True
            elif(b == b'd'):
                self.lightState = False
        
        return self.lightState
    
    def setOpen(self, state : bool):
        self.makeSerialAvail()

        self.port.write(b'o' if state else b'c')
        