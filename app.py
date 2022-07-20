#!/usr/bin/env python
import signal
import os
import asyncio
import websockets

user = set()
wall = set()

async def hello(websocket, path):
    message = await websocket.recv()
    if message == "User":
        user.add(websocket)
        print("User assigned")
    if message == "Wall":
        wall.add(websocket)
        print("Wall assigned")
    await websocket.send(message)

    while True:

        message = await websocket.recv()
        if websocket in user:
            message = "User: " + message
            if wall:
                websockets.broadcast(wall, message)
            else:
                websockets.broadcast(user, "Wall not connected.")
                print("Wall not connected.")
        else:
            message = "Non-user: " + message

        print(message)
        #await websocket.send(message)


async def main():
    # Set the stop condition when receiving SIGTERM.
    loop = asyncio.get_running_loop()
    stop = loop.create_future()
    loop.add_signal_handler(signal.SIGTERM, stop.set_result, None)

    async with websockets.serve(
            hello,
            host="",
            port=int(os.environ["PORT"]),
    ):
        await stop
if __name__ == "__main__":
    asyncio.run(main())