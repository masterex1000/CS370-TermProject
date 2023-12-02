import asyncio
from microdot_asyncio import Microdot
from webapi import blindapi

app = Microdot()

@app.route('/')
async def hello(request):
    return 'Hello, world!'

app.mount(blindapi, url_prefix="/api/blindservice")

async def main():
    await app.start_server(port=20000, debug=True)

asyncio.run(main())