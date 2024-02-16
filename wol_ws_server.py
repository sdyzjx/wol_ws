import websockets
import asyncio
import json
from websockets.legacy.server import WebSocketServerProtocol


class WolSocket:
    port = 8266
    client = {}
    test_state = False

    def __init__(self, _port):
        port = _port
        print("Server started at port " + str(port) + " on localhost")
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

    async def main(self):
        async with websockets.serve(self.ws_handle, "127.0.0.1", self.port):
            await asyncio.Future()
