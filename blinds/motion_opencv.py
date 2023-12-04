from multiprocessing import Process, Queue, current_process, freeze_support
from blindtypes import *
import cv2
import time
import numpy as np

class MotionModule:

    lastMotionTime = 0    
    isMotion = 0

    def __init__(self, inQueue: Queue, outQueue:Queue):
        self.inQueue = inQueue
        self.outQueue = outQueue
        pass

    def run(self):
        vid = cv2.VideoCapture(0) 


        firstFrame = True
        cmpFrame = None

        while True:

            # Implements algo #3
            # https://medium.com/@abbessafa1998/motion-detection-techniques-with-code-on-opencv-18ed2c1acfaf

            ret, frame = vid.read()

            curTime = round(time.time() * 1000)

            frame = cv2.resize(frame, (512, 512))
            gray = cv2.cvtColor(frame, cv2.COLOR_BGR2GRAY)
            gray = cv2.GaussianBlur(gray, (21, 21), 0)

            if(firstFrame):
                firstFrame = False
                cmpFrame = gray
                continue

            diff = cv2.absdiff(cmpFrame, gray)

            ret, motion_mask = cv2.threshold(diff, 60, 255, cv2.THRESH_BINARY)

            cmpFrame = self.update_background(gray, cmpFrame, 0.1)

            # cv2.imshow("motionmask", motion_mask)
            # cv2.imshow("background", cmpFrame)

            n_white_pix = np.sum(motion_mask == 255)


            curMotion = n_white_pix >= 1000

            if curMotion:
                self.lastMotionTime = curTime

            # Only allow use to disable motion if enough time has passed
            if not curMotion and curTime - self.lastMotionTime < 4000:
                curMotion = True

            if curMotion != self.isMotion:
                self.isMotion = curMotion

                self.outQueue.put(
                    BlindEvent(
                        BlindEventType.VALUE_UPDATE, 
                        BlindEventChangeValue(BlindValueId.motion, self.isMotion)))

            # cv2.imshow('frame', gray)
    
        vid.release()
        cv2.destroyAllWindows()

    
    def update_background(self, current_frame, prev_bg, alpha):
        bg = alpha * current_frame + (1 - alpha) * prev_bg
        bg = np.uint8(bg)
        return bg

    def checkContours(self, countour) -> bool:
        for i in countour:
            if cv2.contourArea(i) < 50:
                return True
        
        return False