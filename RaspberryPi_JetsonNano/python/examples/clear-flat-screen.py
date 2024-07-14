#!/usr/bin/python
# -*- coding:utf-8 -*-
import sys
import os
import asyncio
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

logging.basicConfig(level=logging.INFO)

async def connect():
    try:
        logging.info("epd2in13_V4 Demo")

        epd = epd2in13d.EPD()
        logging.info("init and Clear")
        epd.init()
        epd.Clear()

    except IOError as e:
        logging.info(e)

    except KeyboardInterrupt:
        logging.info("ctrl + c:")
        epd2in13d.epdconfig.module_exit(cleanup=True)
        exit()

if __name__ == "__main__":
    asyncio.get_event_loop().run_until_complete(connect())