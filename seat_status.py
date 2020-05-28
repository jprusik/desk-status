import adafruit_ssd1306
import busio
import json
import os
import requests
import subprocess
import time
from board import SCL, SDA
from datetime import datetime
from PIL import Image, ImageDraw, ImageFont
import robin_api

# Create the I2C interface.
i2c = busio.I2C(SCL, SDA)

# Create the SSD1306 OLED class.
# The first two parameters are the pixel width and pixel height.  Change these
# to the right size for your display!
disp = adafruit_ssd1306.SSD1306_I2C(128, 64, i2c)

# flip the display upside down because that's how I mounted it
disp.rotation = 2

height = disp.height
width = disp.width
padding = -2
top = padding
bottom = height-padding
x = 0

# Make sure to create image with mode '1' for 1-bit color.
image = Image.new('1', (width, height))

# Get drawing object to draw on image.
draw = ImageDraw.Draw(image)

# Load default font
# font = ImageFont.load_default()

# Load TTF fonts
font = ImageFont.truetype('./fonts/UbuntuMono-B.ttf', 16)
alt_font = ImageFont.truetype('./fonts/UbuntuMono-R.ttf', 16)
small_font = ImageFont.truetype('./fonts/Ubuntu-C.ttf', 13)

def update_seat():
    # Draw a black filled box to clear the image.
    draw.rectangle((0, 0, width, height), outline=0, fill=0)

    robin_seat = robin_api.get_reservees_by_seat()

    reservations = robin_seat['data']
    seat_name = ''
    seat_zone = ''
    reservee_name = ''
    seat_type = ''
    seat_disabled = False
    seat_reservable = True
    reservee_avatar = ''

    # lazy property diving
    if len(reservations):
        try:
            seat_name = reservations[0]['seat']['name']
        except:
            pass
        try:
            seat_zone = reservations[0]['seat']['zone']['name']
        except:
            pass
        try:
            reservee_name = reservations[0]['reservee']['user']['name']
        except:
            pass
        try:
            seat_type = reservations[0]['type']
        except:
            pass
        try:
            seat_disabled = reservations[0]['seat']['is_disabled']
        except:
            pass
        try:
            seat_reservable = reservations[0]['seat']['is_reservable']
        except:
            pass
        try:
            reservee_avatar = reservations[0]['reservee']['user']['avatar']
        except:
            pass

        draw.text((x, top), ', '.join((seat_name, seat_zone)),  font=alt_font, fill=255)

        if seat_type == 'assigned':
            if reservations[0]['reservee']['email'] is not None:
                draw.text((x, top+16), 'This seat is assigned to:',  font=small_font, fill=255)
                draw.text((x, top+16+13+2), reservee_name, font=font, fill=255)
            elif seat_disabled is True:
                draw.text((x, top+16), 'This seat is:',  font=small_font, fill=255)
                draw.text((x, top+16+13+2), 'UNAVAILABLE', font=font, fill=255)
            else:
                draw.text((x, top+16), 'This seat is:',  font=small_font, fill=255)
                draw.text((x, top+16+13+2), 'AVAILABLE', font=font, fill=255)

    else:
        robin_seat = robin_api.get_seat()

        if robin_seat is None:
            draw.text((x, top+16), 'ERROR',  font=font, fill=255)
        else:
            try:
                seat_name = robin_seat['data']['name']
            except:
                pass
            try:
                seat_zone = robin_seat['data']['zone']['name']
            except:
                pass
            try:
                seat_disabled = robin_seat['data']['is_disabled']
            except:
                pass
            try:
                seat_reservable = robin_seat['data']['is_reservable']
            except:
                pass

            draw.text((x, top), ', '.join((seat_name, seat_zone)),  font=alt_font, fill=255)
            draw.text((x, top+16), 'This seat is:',  font=small_font, fill=255)

            if seat_disabled is not True:
                draw.text((x, top+16+13+2), 'AVAILABLE', font=font, fill=255)
            else:
                draw.text((x, top+16+13+2), 'UNAVAILABLE', font=font, fill=255)

    # Display image.
    disp.image(image)
    disp.show()

while False:
    update_seat()
    time.sleep(10) # TODO: make this value an environment variable
