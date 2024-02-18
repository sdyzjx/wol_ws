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
import wakeonlan
import aioconsole
import websockets
import json


# TODO: Make this into a class
#       Heartbeat system
#       initialize system: Make user enter the mac address of the target system, the remote server address and client id

class WolClient:
    def __init__(self, _mac, _address, _id):
        self.mac = _mac
        self.address = _address
        self.client_id = _id
        self.state = True
        # fetch initial server config
        # asyncio.run(self.client_start(mac, address, client_id))

    async def client_start(self):
        async with websockets.connect(self.address) as self.ws:
            msg = {
                "id": self.client_id,
                "action": "100"
            }
            json_data = json.dumps(msg)
            await self.ws.send(json_data)
            response = await self.ws.recv()
            json_recv = json.loads(response)
            if "msg" in json_recv:
                msg = json_recv["msg"]
                if msg == "100_1":
                    print("Server " + self.address + " connected succefully.")
                    print("Entering listening mode")
                    await self.recv_handler()

    async def recv_handler(self):
        while True:
            response = await self.ws.recv()
            json_recv = json.loads(response)
            if "msg" in json_recv:
                msg = json_recv["msg"]
                if msg == "200":
                    print("PC start")
                    # wakeonlan.send_magic_packet(self.mac)
                elif msg == "800_1":
                    self.ws.close()
                    self.state = False
                elif msg == "600":
                    msg_re = {
                        "id": self.client_id,
                        "action": "600_1"
                    }
                    json_data = json.dumps(msg_re)
                    await self.ws.send(json_data)

    async def client_stop(self):
        msg = {
            "id": self.client_id,
            "action": "800"
        }
        json_data = json.dumps(msg)
        await self.ws.send(json_data)

    # wol = WolClient("23333", "ws://127.0.0.1:4000", "Mark_1")
    # asyncio.run(wol.client_start())
    async def get_input(self, prompt):
        user_input = await aioconsole.ainput(prompt)
        return user_input

    async def client_control(self):
        print(
            "Please choose action:\n" +
            "--------------------------------\n" +
            "s: Shutdown the client\n" +
            "m: Reconfigure mac address\n" +
            "--------------------------------"
        )
        while True:
            user_input = await self.get_input("Enter command:")
            if not self.state:
                exit()
            if user_input == 's':
                await self.client_stop()
                print("Client has stopped")
                # exit()
            elif user_input == 'm':
                mac_input = await self.get_input("Enter new mac:")
                self.mac = mac_input
