# TODO: develop api system for frontend panel

import time
import asyncio
import wolServer
import apiBackend


async def main():
    ws_socket = wolServer.WolSocket(8266)
    api = apiBackend.apiServer(5432, ws_socket)
    ws_task = asyncio.create_task(ws_socket.start_ws_server())
    api_task = asyncio.create_task(api.start_api_server())
    await asyncio.gather(ws_task, api_task)


if __name__ == '__main__':
    asyncio.run(main())
