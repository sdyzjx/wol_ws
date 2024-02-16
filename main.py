# TODO: develop api system for frontend panel
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
import time
import asyncio
import wol_ws_server


async def handler(socket):
    #
    while True:
        if socket.test_state:
            print("bad decision")
            await socket.sendmsg("Mark_1", "success!!")
            if "Mark_2" in socket.clients:
                await socket.sendmsg("Mark_2", "fuck!!")
            await asyncio.sleep(10)
        else:
            print("socket test success")
            await asyncio.sleep(10)


async def main():
    socket = wol_ws_server.WolSocket(8266)
    server_task = asyncio.create_task(socket.main())
    # 启动WebSocket服务器任务
    listen = asyncio.create_task(handler(socket))
    await asyncio.gather(server_task, listen)


if __name__ == '__main__':
    asyncio.run(main())
