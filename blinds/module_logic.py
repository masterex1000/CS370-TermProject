from multiprocessing import Process, Queue, current_process, freeze_support
from blindtypes import *


def logic_entry(inQueue : Queue, outQueue : Queue):
    c = LogicModule(inQueue, outQueue)

    c.run()
    

class LogicModule:

    values = {
        BlindValueId.light: False,
        BlindValueId.motion: False,

        BlindValueId.time: False, # Indicates time cuttofs

        BlindValueId.override: False,
        BlindValueId.override_state: False,

        BlindValueId.output_state: False     
    }

    def __init__(self, inQueue : Queue, outQueue : Queue):
        self.inQueue = inQueue
        self.outQueue = outQueue
    
    def run(self):
        while True:
            self.processEvents()
    
    def processEvents(self):
        # We can block because we only need to update the state when something changes
        event: BlindEvent = self.inQueue.get()

        self.handleEvent(event)
    
    def handleEvent(self, event: BlindEvent):
        if event.name == BlindEventType.VALUE_UPDATE:
            self.values[event.value.type] = event.value.value
            
            self.executeLogic() #Somethings changed
    
    def executeLogic(self):
        isOpen : bool = False

        if self.values[BlindValueId.override]:
            isOpen = BlindValueId.override_state
        elif self.values[BlindValueId.light] and self.values[BlindValueId.motion]:
            isOpen = True
        
        if self.values[BlindValueId.output_state] != isOpen:
            self.values[BlindValueId.output_state] = isOpen

            self.outQueue.put(
                BlindEvent(
                    BlindEventType.VALUE_UPDATE, 
                    BlindEventChangeValue(BlindValueId.output_state, isOpen)))
