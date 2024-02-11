import websockets
import asyncio
import json
from websockets.legacy.server import WebSocketServerProtocol


class WolSocket:
    port = 8266
    client = {}

    def __init__(self, _port):
        port = _port
        print("Server started at port " + str(port) + " on localhost")
        self.clients = {}
        self.ws_server(port)

    async def ws_handle(self, websocket: WebSocketServerProtocol, path: str):
        async for message in websocket:
            print(message)
            json_recv = json.loads(message)
            msg_send = {}
            if "id" in json_recv:
                id = json_recv["id"]
                action = json_recv["action"]

                if id not in self.clients and action == "100":
                    self.clients[id] = websocket
                    msg_send = {
                        "msg": "100_1"  # Connection established
                    }
                    print("New connection " + id + " established successfully")
                if id in self.clients and action == "800":
                    del self.clients[id]
                    print(id + " disconnected")

            await websocket.send(id)

    async def sendmsg(self, mac, msg):
        # if(websocket in clients):
        websocket = self.clients[mac]
        await websocket.send(msg)

    async def main(self, port):
        async with websockets.serve(self.ws_handle, "127.0.0.1", port):
            await asyncio.Future()

    def ws_server(self, port):
        asyncio.run(self.main(port))
