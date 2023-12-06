import asyncio
import queue
from multiprocessing import Process, Queue, current_process, freeze_support
from blindtypes import *
from microdot_asyncio import Microdot, Response
from microdot_jinja import render_template
import time
#### Global Variables

outputState = "" #variable for output state
timeClosed = 0
timeOpen = 0
mockStart = time.time()
startTime = time.time()
# These will be updated as they change
values = {
    BlindValueId.light: False,
    BlindValueId.motion: False,

    BlindValueId.time: False, # Indicates time cuttofs

    BlindValueId.override: False,
    BlindValueId.override_state: False,

    BlindValueId.output_state: False     
}

#### Hook

# called every time a value is changed (great place to add logging logic...)
def valueUpdated(name : BlindValueId, value : bool):
    pass
 


#### Creating the web api

### Webapi

blindapi = Microdot()

#processing for page reset
@blindapi.route("/", methods= ['GET', 'POST'])
async def index(request):

    heatDeflected = 0.0
    # logic for Displaying output state
    if (values[BlindValueId.output_state] == True):
        outputState = "Open"
    else:
        outputState = "Closed"
    global timeClosed
    global timeOpen
    global startTime
    global mockStart

    if (values[BlindValueId.output_state] == False):
        timeClosed += time.time() - mockStart 
    elif (values[BlindValueId.output_state] == True):
        timeOpen += time.time() - mockStart
    mockStart = time.time()
    
    #logic for calculating time 
    # 0.45 is proportion of head that is deflected form blinds full down 100% of time
    heatDeflected = 0.45 * (timeClosed / (time.time() - startTime))
    

    
    return render_template('index.html', status = outputState, totalClose = heatDeflected * 100)

### App
app = Microdot()
Response.default_content_type = 'text/html'


@app.route('/')
#main request for home page of app
async def hello(request):
    return 'Hello world' 
#request to set manual mode to true


app.mount(blindapi, url_prefix="/api/blindservice")


#### Event Handler (handles the events comming off the wire)

class EventsHandler:

    def __init__(self, inQueue : Queue, outQueue : Queue):
        self.inQueue = inQueue
        self.outQueue = outQueue
    
    async def run(self):
        while True:
            self.processEvents()
            await asyncio.sleep(0.1) # Only run 10 times a second
        
    def processEvents(self):
        try:
            while True: # Process events till no more
                event: BlindEvent = self.inQueue.get_nowait()
                self.handleEvent(event)

        except queue.Empty:
            return # Queue empty now
    
    def handleEvent(self, event: BlindEvent):
        if event.name == BlindEventType.VALUE_UPDATE:
            values[event.value.type] = event.value.value
            valueUpdated(event.value.type, event.value.value)

#### Entry Point 

# Entry point from main, runs in a seperate process
def webserver_entry(inQueue : Queue, outQueue : Queue):
    asyncio.run(main(inQueue, outQueue))

async def main(inQueue : Queue, outQueue : Queue):
    asyncio.create_task(doEvents(inQueue, outQueue))
    await app.start_server(port=20000, debug=True)

async def doEvents(inQueue : Queue, outQueue : Queue):
    h = EventsHandler(inQueue, outQueue)
    await h.run()
