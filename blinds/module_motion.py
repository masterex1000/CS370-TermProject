from multiprocessing import Process, Queue, current_process, freeze_support
import os

if os.environ.get('USE_CAMERA') == 'True':
    print("INFO: Using motion_opencv for MotionModule")
    from motion_opencv import MotionModule
else:
    print("INFO: Using motion_fake for MotionModule")
    from motion_fake import MotionModule

def motion_entry(inQueue : Queue, outQueue : Queue):
    
    m = MotionModule(inQueue, outQueue)
    m.run()

    pass