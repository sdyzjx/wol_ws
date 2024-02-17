import json
from aiohttp import web
import wolServer as ws

"""
request format:
    Receive: {
        action:
            400: get online machine list
            500: PC poweron request {
                parameter:
                    client_id
    }
    Send: {
        msg:
            500_1: Poweron request sent success
            400_1: get online machine success {
                parameter: client_id_list
            }
    }
"""


class apiServer:
    def __init__(self, _port: int, _socket: ws.WolSocket):
        self.port = _port
        self.socket = _socket

    async def handle_api_request(self, request):
        data = await request.json()
        action = data.get('action')
        if action == "400":
            # return machine list
            client_id_list = list(self.socket.client.values())
            # client_id_list_json = json.dumps(client_id_list)
            response = {
                "msg": "400_1",
                "client_list": client_id_list
            }
            response_json = json.dumps(response)
            print("Clients list successfully checked.")
            return web.json_response(response_json)

        elif action == "500":
            client_id = data.get('client_id')
            if client_id in self.socket.client:
                await self.socket.sendmsg(client_id, "200")
                print("Client " + client_id + " power on request sent successfully.")
                response = {
                    "msg": "500_1"
                }
                response_json = json.dumps(response)
                return web.json_response(response_json)
            else:
                print("invalid client id. pls try again")

    async def start_api_server(self):
        app = web.Application()
        app.add_routes([web.post('/wol', self.handle_api_request)])
        runner = web.AppRunner(app)
        await runner.setup()
        site = web.TCPSite(runner, 'localhost', self.port)
        await site.start()
        print("api server started at port " + str(self.port) + " on localhost")
