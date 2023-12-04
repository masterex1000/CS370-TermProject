from multiprocessing import Process, Queue, current_process, freeze_support
from blindtypes import *
import os
import time

class MotionModule:

    lastMotionTime = 0    
    isMotion = 0

    def __init__(self, inQueue: Queue, outQueue:Queue):
        self.inQueue = inQueue
        self.outQueue = outQueue
        pass

    def run(self):

        while True:
            time.sleep(3)
            self.sendMotionStatus(True)
            time.sleep(3)
            self.sendMotionStatus(False)
    
    def sendMotionStatus(self, isMotion : bool):
        self.outQueue.put(
            BlindEvent(
                BlindEventType.VALUE_UPDATE, 
                BlindEventChangeValue(BlindValueId.motion, isMotion)))