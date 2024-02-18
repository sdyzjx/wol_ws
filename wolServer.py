"""
Response structure:
    action:
        200: start PC
        100_1: connected successfully
        800_1: disconnected successfully
        600_1: Heartbeat success

Post structure:
    action:
        100: Start connection
        800: Stop connection
        600: Heartbeat pack
    id: id of the client machine (entered by user)

"""
import time

import websockets
import asyncio
import json
from websockets.legacy.server import WebSocketServerProtocol


class WolSocket:
    client = {}
    test_state = False

    def __init__(self, _port):
        self.port = _port
        print("Websocket server started at port " + str(self.port) + " on localhost")
        self.clients = {}

    async def ws_handle(self, websocket: WebSocketServerProtocol, path: str):
        async for message in websocket:
            print(message)
            json_recv = json.loads(message)
            if "id" in json_recv:
                id = json_recv["id"]
                action = json_recv["action"]

                if id not in self.clients and action == "100":
                    self.clients[id] = websocket
                    msg_send = {
                        "msg": "100_1"  # Connection established
                    }
                    json_data = json.dumps(msg_send)
                    print("New connection " + id + " established successfully")
                    await websocket.send(json_data)
                    self.test_state = True
                if id in self.clients and action == "800":
                    del self.clients[id]
                    print(id + " disconnected")


    async def sendmsg(self, client_id, msg):
        # if(websocket in clients):
        msg_send = {
            "msg": msg
        }
        json_data = json.dumps(msg_send)
        websocket = self.clients[client_id]
        await websocket.send(json_data)

    async def start_ws_server(self):
        async with websockets.serve(self.ws_handle, "127.0.0.1", self.port):
            await asyncio.Future()

    async def heart_beat(self):
        while True:
            for client in self.clients:
                ws_temp = client.value()
                msg_send = {
                    "msg": "600"
                }
                json_data = json.dumps(msg_send)
                try:
                    await ws_temp.send(json_data)
                except:
                    del self.clients[client.key()]

            time.sleep(2)
