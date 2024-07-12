import asyncio
import websockets
from parse_object import parse_object

config = {
    "url": "wss://webserver14.sms-timing.com:10015/",
    "initWSMessage": "START 19476@teamsportdocklands",
    "driverName": "Greg",
    "headers": {
        "Pragma": "no-cache",
        "Accept": "*/*",
        "Sec-WebSocket-Key": "2JpCv",
        "Sec-Fetch-Site": "cross-site",
        "Sec-WebSocket-Version": "13",
        "Sec-WebSocket-Extensions": "permessage-deflate",
        "Cache-Control": "no-cache",
        "Sec-Fetch-Mode": "websocket",
        "Accept-Language": "en-GB,en;q=0.9",
        "Origin": "ionic://localhost",
        "User-Agent":
            "Mozilla/5.0 (iPhone; CPU iPhone OS 17_5_1 like Mac OS X) AppleWebKit/605.1.15 (KHTML, like Gecko) Mobile/15E148",
        "Connection": "Upgrade",
        "Accept-Encoding": "gzip, deflate",
        "Upgrade": "websocket",
        "Sec-Fetch-Dest": "websocket",
    },
}

initWSMessage = config['initWSMessage']
headers = config['headers']
url = config['url']


async def connect():
    async with websockets.connect(url) as ws:
        print("Connected to the server")
        await ws.send(initWSMessage)

        while True:
            try:
                data = await ws.recv()
                parse_object(data, 'Docklands Kart 4')
            except websockets.exceptions.ConnectionClosed:
                print("Disconnected from the server")
                break
            except Exception as error:
                print("WebSocket error:", error)
                break


if __name__ == "__main__":
    asyncio.get_event_loop().run_until_complete(connect())
