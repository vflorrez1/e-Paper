#!/usr/bin/python
# -*- coding:utf-8 -*-
import sys
import os
import asyncio
import json
import websockets
from parse_object import parse_object


config = {
    "url": "wss://webserver14.sms-timing.com:10015/",
    "initWSMessage": "START 19476@teamsportdocklands",
    "driverName": "Afam",
}

initWSMessage = config['initWSMessage']
url = config['url']
driver_name = config['driverName']

picdir = os.path.join(os.path.dirname(os.path.dirname(os.path.realpath(__file__))), 'pic')
libdir = os.path.join(os.path.dirname(os.path.dirname(os.path.realpath(__file__))), 'lib')
if os.path.exists(libdir):
    sys.path.append(libdir)

import logging
from waveshare_epd import epd2in13d
from PIL import Image, ImageDraw, ImageFont

logging.basicConfig(level=logging.INFO)

async def connect():
    try:
        logging.info("epd2in13_V4 Demo")

        epd = epd2in13d.EPD()
        logging.info("init and Clear")
        epd.init()
        epd.Clear()

        # Drawing on the image
        font1 = ImageFont.truetype(os.path.join(picdir, 'Font.ttc'), 18)
        screen_width = epd.height
        screen_height = epd.width

        y_top, y_bottom = 0, screen_height
        y_mid = y_bottom / 2

        top_line_1 = 50
        top_line_2 = (screen_width + top_line_1) / 2
        top_half_line_height = 20
        bottom_half_line_height = 80

        # # partial update
        logging.info("Vics test time...")
        time_image = Image.new('1', (epd.height, epd.width), 255)
        draw = ImageDraw.Draw(time_image)
        # epd.displayPartBaseImage(epd.getbuffer(time_image))
        name = driver_name

        def draw_text(cords, text):
            draw.text(cords, text, font=font1, fill='black')

        async with websockets.connect(url) as ws:
            print("Connected to the server")
            await ws.send(initWSMessage)

            try:
                driver_d = await ws.recv()
                jsn_data = json.loads(driver_d)
                name = jsn_data['D'][0]['N']
            except Exception as error:
                    print("could not get random name")    
            
            while (True):
                try:
                    data = await ws.recv()
                    # OVVERIDE THE NAME OF THE DRIVER HERE
                    all_data = parse_object(data, name) # ++++++++++++++++++++++++++++++++++++++++++++++++
                    racer_data = all_data['racer']
                    session_data = all_data['session']

                    # mask rect
                    draw.rectangle([(0, y_top), (screen_width, y_bottom)], fill=225)
                    if racer_data is None:
                        draw_text((15, top_half_line_height), 'Racer not found')
                        draw_text((15, bottom_half_line_height), session_data['sessionCountDown'])

                        # find another random driver
                        jsn_d = json.loads(data)
                        if jsn_d and len(jsn_d['D']) > 0:
                            name = jsn_d['D'][0]['N']
                    elif session_data['sessionCountDown'] == '00:00':
                        draw_text((15, top_half_line_height), 'Session Ended')   
                    else:          
                        print("Racer Data:")
                        print(json.dumps(racer_data, indent=4))

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
                        draw_text((15, top_half_line_height), 'P' + str(racer_data['position']))

                        # last lap
                        draw_text((70, top_half_line_height), racer_data['currentLapTime'])

                        # delta
                        draw_text((170, top_half_line_height), racer_data['delta'])

                        # best lap
                        draw_text((145, bottom_half_line_height), racer_data['bestLapTime'])

                        # count down
                        draw_text((17, bottom_half_line_height), session_data['sessionCountDown'])

                    epd.DisplayPartial(epd.getbuffer(time_image))
                except websockets.exceptions.ConnectionClosed:
                    print("Disconnected from the server")
                    break
                except Exception as error:
                    print("WebSocket error:", error)
                    break  

        logging.info("Clear...")
        epd.init()
        epd.Clear()

        logging.info("Goto Sleep...")
        epd.sleep()

    except IOError as e:
        logging.info(e)

    except KeyboardInterrupt:
        logging.info("ctrl + c:")
        epd2in13d.epdconfig.module_exit(cleanup=True)
        exit()

if __name__ == "__main__":
    asyncio.get_event_loop().run_until_complete(connect())