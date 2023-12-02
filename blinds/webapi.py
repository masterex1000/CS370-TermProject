from microdot_asyncio import Microdot

blindapi = Microdot()

@blindapi.get("/")
async def hello(request):
    return "Not Implemented", 501