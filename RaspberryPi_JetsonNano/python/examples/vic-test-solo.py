#!/usr/bin/python
# -*- coding:utf-8 -*-
import sys
import os
picdir = os.path.join(os.path.dirname(os.path.dirname(os.path.realpath(__file__))), 'pic')
libdir = os.path.join(os.path.dirname(os.path.dirname(os.path.realpath(__file__))), 'lib')
if os.path.exists(libdir):
    sys.path.append(libdir)

import logging
from waveshare_epd import epd2in13_V4
import time
from PIL import Image,ImageDraw,ImageFont
import traceback

logging.basicConfig(level=logging.DEBUG)

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
    num = 0
    while (True):
        # count down
        draw.rectangle((120, 80, 220, 105), fill = 255)
        draw.text((17, bottom_half_line_height), time.strftime('%H:%M:%S'), fill='black', font=font1)
        epd.displayPartial(epd.getbuffer(time_image))
        num = num + 1
        if(num == 20):
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
