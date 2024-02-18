import asyncio

import wolClient as wol


async def main(mac, server, client_id):
    ws_socket = wol.WolClient(mac, server, client_id)
    ws_task = asyncio.create_task(ws_socket.client_start())
    client_task = asyncio.create_task(ws_socket.client_control())
    await asyncio.gather(ws_task, client_task)


if __name__ == '__main__':
    mac = input("Please enter the mac address of your target machine:")
    server = input("Please enter the url of your ws server:")
    client_id = input("Please decide a client id:")
    asyncio.run(main(mac, server, client_id))
