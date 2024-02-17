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
#       initialize system: Make user enter the mac address of the target system, the remote server address and client id

class WolClient:
    def __init__(self, _mac, _address, _id):
        mac = _mac
        address = _address
        client_id = _id

        # fetch initial server config
        asyncio.run(self.client_start(mac, address, client_id))

    async def client_start(self, mac, address, client_id):
        async with websockets.connect(address) as ws:
            msg = {
                "id": client_id,
                "action": "100"
            }
            json_data = json.dumps(msg)
            await ws.send(json_data)
            response = await ws.recv()
            json_recv = json.loads(response)
            if "msg" in json_recv:
                msg = json_recv["msg"]
                if msg == "100_1":
                    print("Server " + address + " connected succefully.")
                    print("Entering listening mode")
                    await self.recv_handler(ws)

    async def recv_handler(self, ws):
        while True:
            response = await ws.recv()
            json_recv = json.loads(response)
            if "msg" in json_recv:
                msg = json_recv["msg"]
                print(msg)


wol = WolClient("23333", "ws://127.0.0.1:8266", "Mark_1")
