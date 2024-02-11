"""
Response structure:
    action:
        200: start PC
        100_1: connected successfully
        800_1: disconnected successfully

Post structure:
    action:
        100: Start connection
        800: Stop connection
    id: id of the client machine (entered by user)

"""

import asyncio
import websockets
import json

# TODO: Make this into a class
#       Heartbeat system
#       __init__(): Establish a connection
#       __del__(): Disconnect
#       recv_handler(): Handle the msg recv, use wol to start computer
#       initialize system: Make user enter the mac address of the target system, the remote server address and client id


async def hello():
    async with websockets.connect("ws://localhost:8266") as websocket:
        msg = {
            "mac": "test",
            "action": "800"
        }
        json_data = json.dumps(msg)
        await websocket.send(json_data)
        response = await websocket.recv()
        print(response)
        # run forever, wating for action
        while True:
            msg = await websocket.recv()


asyncio.run(hello())
