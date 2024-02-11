import asyncio
import websockets
import json

async def hello():
    async with websockets.connect("ws://localhost:8266") as websocket:
        msg = {
            "mac": "fuck",
            "client": "23333"
        }
        json_data = json.dumps(msg)
        await websocket.send(json_data)
        response = await websocket.recv()
        print(response)

asyncio.run(hello())