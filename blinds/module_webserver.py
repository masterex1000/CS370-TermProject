from multiprocessing import Process, Queue, current_process, freeze_support
import queue
import asyncio
from microdot_asyncio import Microdot
from blindtypes import *


### Webapi

blindapi = Microdot()

@blindapi.get("/")
async def hello(request):
    return "Not Implemented", 501

### App

app = Microdot()

@app.route('/')
async def hello(request):
    return 'Hello, world!'

app.mount(blindapi, url_prefix="/api/blindservice")

async def main():
    await app.start_server(port=20000, debug=True)


# Entry point from main, runs in a seperate process
def webserver(inQueue : Queue, outQueue : Queue):
    asyncio.run(main())