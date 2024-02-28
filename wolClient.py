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
        600: Reconnect
        700: heartbeat
    id: id of the client machine (entered by user)

"""

import asyncio
from datetime import *
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
        self.shutdown_state = False
        self.connected = False
        self.retries = -1
        self.heartbeat = False
        # fetch initial server config
        # asyncio.run(self.client_start(mac, address, client_id))

    async def heartbeat_send(self):
        msg = json.dumps({"id": self.client_id, "action": "700",
                          "time": datetime.utcnow().strftime("%Y-%m-%d %H:%M:%S")})
        json_msg = json.dumps(msg)
        await self.ws.send(json_msg)

    async def heartbeat_handler(self):
        while self.connected:
            if self.connected:
                await asyncio.sleep(3)
                await self.heartbeat_send()

    async def client_control(self):
        while True:
            # 发现没有连接进入重连模式
            if not self.connected:
                if self.retries == -1:
                    await self.client_start()
                else:
                    print("Strat reconnection")
                    await self.reconnect_server()

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
                    self.connected = True
                    self.retries = 0
                    await self.recv_handler()

    async def recv_handler(self):
        while self.connected:
            try:
                response = await self.ws.recv()
                json_recv = json.loads(response)
                if "msg" in json_recv:
                    msg = json_recv["msg"]
                    if msg == "200":
                        print("PC start")
                        wakeonlan.send_magic_packet(self.mac)
                    elif msg == "800_1":
                        await self.ws.close()
                        self.shutdown_state = True
                        exit()

                    '''
                        elif msg == "600":
                        msg_re = {
                            "id": self.client_id,
                            "action": "600_1"
                        }
                        json_data = json.dumps(msg_re)
                        await self.ws.send(json_data)
                    '''

            except Exception as e:
                print(e)
                self.connected = False

            # else:
            #     if self.retries >= 30:
            #         self.shutdown_state = True
            #         exit()
            #     print("Connection error occurred, reconnecting...")
            #     await self.reconnect_server()

    async def reconnect_server(self):
        try:
            async with websockets.connect(self.address) as ws_t:
                msg = {
                    "id": self.client_id,
                    "action": "600"
                }
                json_data = json.dumps(msg)
                await ws_t.send(json_data)
                response = await ws_t.recv()
                json_recv = json.loads(response)
                if "msg" in json_recv:
                    msg = json_recv["msg"]
                    if msg == "600_1":
                        print("Server " + self.address + " reconnected succefully.")
                        self.connected = True
                        self.retries = 0
                        self.ws = ws_t
                        await self.recv_handler()
        except Exception as e:
            print("Reconnection failed, tried " + str(self.retries) + " times")
            self.retries = self.retries + 1

    async def client_stop(self):
        msg = {
            "id": self.client_id,
            "action": "800"
        }
        json_data = json.dumps(msg)
        await self.ws.send(json_data)

    async def get_input(self, prompt):
        user_input = await aioconsole.ainput(prompt)
        return user_input

    async def input_control(self):
        print(
            "Please choose action:\n" +
            "--------------------------------\n" +
            "s: Shutdown the client\n" +
            "m: Reconfigure mac address\n" +
            "--------------------------------"
        )
        while True:
            user_input = await self.get_input("Enter command:")
            if user_input == 's':
                await self.client_stop()
                print("Client has stopped")
                # exit()
            elif user_input == 'm':
                mac_input = await self.get_input("Enter new mac:")
                self.mac = mac_input
            if self.shutdown_state:
                exit()
