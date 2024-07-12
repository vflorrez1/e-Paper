#!/usr/bin/python
# -*- coding:utf-8 -*-
import sys
import os
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

picdir = os.path.join(os.path.dirname(os.path.dirname(os.path.realpath(__file__))), 'pic')
libdir = os.path.join(os.path.dirname(os.path.dirname(os.path.realpath(__file__))), 'lib')
if os.path.exists(libdir):
    sys.path.append(libdir)

import logging
from waveshare_epd import epd2in13_V4
import time
from PIL import Image, ImageDraw, ImageFont

logging.basicConfig(level=logging.DEBUG)

async def connect():
    try:
        logging.info("epd2in13_V4 Demo")

        epd = epd2in13_V4.EPD()
        logging.info("init and Clear")
        epd.init()
        epd.Clear(0xFF)

        # Drawing on the image
        font1 = ImageFont.truetype(os.path.join(picdir, 'Font.ttc'), 24)
        screen_width = epd.height
        screen_height = epd.width

        y_top, y_bottom = 0, 122
        y_mid = y_bottom / 2

        top_line_1 = 50
        top_line_2 = (screen_width + top_line_1) / 2
        top_half_line_height = 20
        bottom_half_line_height = 80

        # # partial update
        logging.info("Vics test time...")
        time_image = Image.new('1', (epd.height, epd.width), 255)
        draw = ImageDraw.Draw(time_image)
        epd.displayPartBaseImage(epd.getbuffer(time_image))
        async with websockets.connect(url) as ws:
            print("Connected to the server")
            await ws.send(initWSMessage)
            
            while (True):
                try:
                    data = await ws.recv()
                    all_data = parse_object(data, 'Paul Bazooka')
                    racer_data = all_data['racer']
                    session_data = all_data['session']
                    # mask rect
                    draw.rectangle([(0, y_top), (screen_width, y_bottom)], fill=225)
                    if racer_data is None:
                        draw.text((15, top_half_line_height), 'Racer not found', fill='black', font=font1)
                        # draw.text((15, bottom_half_line_height), session_data['sessionCountDown'], fill='black', font=font1)
                    elif session_data['sessionCountDown'] == '0:0':
                        draw.text((15, top_half_line_height), 'Session Ended', fill='black', font=font1)   
                    else:          
                        print(racer_data)

                        # top rect
                        draw.rectangle([(0, y_top), (screen_width, y_mid)], outline=0)

                        # top first line
                        draw.line([(top_line_1, y_top), (top_line_1, y_mid)], fill=0, width=1)

                        # top second line
                        draw.line([(top_line_2, 0), (top_line_2, y_mid)], fill=0, width=1)

                        # bottom rect
                        draw.rectangle([(0, y_mid), (screen_width, y_bottom)], outline=0)

                        draw.line([(screen_width / 2, y_mid), (screen_width / 2, y_bottom)], fill=0, width=1)

                        # position
                        draw.text((15, top_half_line_height), 'P' + str(racer_data['position']), fill='black', font=font1)

                        # last lap
                        draw.text((70, top_half_line_height), racer_data['currentLapTime'], fill='black', font=font1)

                        # delta
                        draw.text((170, top_half_line_height), racer_data['delta'], fill='black', font=font1)

                        # best lap
                        draw.text((145, bottom_half_line_height), racer_data['bestLapTime'], fill='black', font=font1)

                        # count down
                        draw.text((17, bottom_half_line_height), session_data['sessionCountDown'], fill='black', font=font1)
                    epd.displayPartial(epd.getbuffer(time_image))
                except websockets.exceptions.ConnectionClosed:
                    print("Disconnected from the server")
                    break
                except Exception as error:
                    print("WebSocket error:", error)
                    break  

        logging.info("Clear...")
        epd.init()
        epd.Clear(0xFF)

        logging.info("Goto Sleep...")
        epd.sleep()

    except IOError as e:
        logging.info(e)

    except KeyboardInterrupt:
        logging.info("ctrl + c:")
        epd2in13_V4.epdconfig.module_exit(cleanup=True)
        exit()

if __name__ == "__main__":
    asyncio.get_event_loop().run_until_complete(connect())