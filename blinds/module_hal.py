from multiprocessing import Process, Queue, current_process, freeze_support
import time
import queue
from blindtypes import *
import os

from hal_serial import BlindHal

# This is run in a seperate process
#   inputQueue: the queue this hal receives events on
#   outputQueue: the queue this module outputs evens on
def hal(inputQueue : Queue, outputQueue : Queue):

    bhal = BlindHal()

    isLight = False

    while True:
        processEvents(inputQueue, bhal)

        light = bhal.isLight()
        if(light != isLight):
            # The light state has changed and we need to update it
            isLight = light

            # Notify the rest of the application
            outputQueue.put(
                BlindEvent(
                    BlindEventType.VALUE_UPDATE, 
                    BlindEventChangeValue(BlindValueId.light, isLight)))

        time.sleep(0.2) # Should be good?


# Attempts to process events 
def processEvents(inputQueue, bhal : BlindHal):
    try:
        # The sentinal value for iter will never be hit, instead get_nowait will throw an
        # exception and stop the loop
        for event in iter(inputQueue.get_nowait, None):
            handleEvent(event, bhal)
    except queue.Empty:
        pass

def handleEvent(event: BlindEvent, bhal : BlindHal):
    # for some reason python doesn't support 
    # switch statments until 3.10 (And I have 3.9)
    # so ig we have to use a chain of if..elif

    if event.name == BlindEventType.DEBUG_PRINT:
        print(event.value)
        return
    elif event.name == BlindEventType.VALUE_UPDATE:
        info : BlindEventChangeValue = event.value
        
        if(info.type == BlindValueId.output_state):
            bhal.setOpen(info.value)
            