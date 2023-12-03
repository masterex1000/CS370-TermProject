import time
from multiprocessing import Process, Queue, current_process, freeze_support
from blindtypes import BlindEvent
from module_hal import hal
from module_webserver import webserver
from module_logic import logic_entry
from module_motion import motion_entry

def main():
    MODULES = [ hal, webserver, logic_entry, motion_entry ]

    # define our message queues
    moduleQueues = [Queue() for i in range(len(MODULES))]
    inQueue = Queue() # Queue our thread will receive events on


    # Start all of the modules
    for i, module in enumerate(MODULES):
        Process(target=module, args=(moduleQueues[i], inQueue)).start()

    #moduleQueues[0].put(BlindEvent("print", "hello world"))


    while True:
        event : BlindEvent = inQueue.get()
        sendToAll(moduleQueues, event)

def sendToAll(moduleQueues, event : BlindEvent):
    for m in moduleQueues:
        m.put(event)

if __name__ == '__main__':
    freeze_support()
    main()