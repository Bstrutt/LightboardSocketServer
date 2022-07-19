#!/usr/bin/env python

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
    start_server = websockets.serve(hello, port=(os.environ["PORT"]), ping_timeout=None)
    asyncio.get_event_loop().run_until_complete(start_server)
    asyncio.get_event_loop().run_forever()

if __name__ == "__main__":
    asyncio.run(main())