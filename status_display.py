import adafruit_ssd1306
import busio
import json
import os
from os.path import join, dirname
import requests
import subprocess
import time
from board import SCL, SDA
from datetime import datetime
from dateutil import parser
from PIL import Image, ImageDraw, ImageFont
import robin_api
import status_light

# Create the I2C interface.
i2c = busio.I2C(SCL, SDA)

# Create the SSD1306 OLED class.
# The first two parameters are the pixel width and pixel height.  Change these
# to the right size for your display!
display = adafruit_ssd1306.SSD1306_I2C(128, 64, i2c)

# flip the display 180º if needed
# display.rotation = 2

height = display.height
width = display.width
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
font = ImageFont.truetype(join(dirname(__file__), 'fonts/UbuntuMono-B.ttf'), 16)
alt_font = ImageFont.truetype(join(dirname(__file__), 'fonts/UbuntuMono-R.ttf'), 16)
small_font = ImageFont.truetype(join(dirname(__file__), 'fonts/Ubuntu-C.ttf'), 13)

def draw_reset():
    draw.rectangle((0, 0, width, height), outline=0, fill=0)
    display.image(image)

def update_seat():
    # Draw a black-filled box to clear the image.
    draw.rectangle((0, 0, width, height), outline=0, fill=0)

    seat_reservation_request = robin_api.get_reservations_by_seat()

    reservations = seat_reservation_request['data']
    seat_name = ''
    seat_zone = ''
    reservee_name = ''
    seat_type = ''
    seat_disabled = False
    seat_reservable = True

    line_one = ''
    line_two = ''
    line_three = ''

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

        line_one = ', '.join((seat_name, seat_zone))
        start = parser.isoparse(reservations[0]['start']['date_time'])
        now = datetime.now().astimezone().replace(microsecond=0)
        active_reservation = now > start

        # If the seat is not assigned, make sure the end of the reservation
        # is also not in the past
        if reservations[0]['end'] is not None:
            end = parser.isoparse(reservations[0]['end']['date_time'])
            active_reservation = now > start and now < end

        if active_reservation is True:
            if reservations[0]['reservee']['email'] is not None:
                line_two = 'This seat is assigned to:'
                line_three = reservee_name
                status_light.set_status('UNAVAILABLE')
            elif seat_disabled is True or seat_reservable is False:
                line_two = 'This seat is:'
                line_three = 'UNAVAILABLE'
                status_light.set_status('UNAVAILABLE')
            else:
                line_two = 'This seat is:'
                line_three = 'UNAVAILABLE'
                status_light.set_status('AVAILABLE')

    else:
        seat_request = robin_api.get_seat()

        if seat_request is None or len(seat_request['data']) == 0:
            draw.text((x, top+16), 'ERROR',  font=font, fill=255)
            line_three = 'DESK NOT FOUND'
        else:
            try:
                seat_name = seat_request['data']['name']
            except:
                pass
            try:
                seat_zone = seat_request['data']['zone']['name']
            except:
                pass
            try:
                seat_disabled = seat_request['data']['is_disabled']
            except:
                pass
            try:
                seat_reservable = seat_request['data']['is_reservable']
            except:
                pass

            line_one = ', '.join((seat_name, seat_zone))
            line_two = 'This seat is:'

            if seat_disabled is not True and seat_reservable is True:
                line_three = 'AVAILABLE'
                status_light.set_status('AVAILABLE')
            else:
                line_three = 'UNAVAILABLE'
                status_light.set_status('UNAVAILABLE')

    if len(line_one):
        draw.text((x, top), line_one,  font=alt_font, fill=255)
    if len(line_two):
        draw.text((x, top+16), line_two,  font=small_font, fill=255)
    if len(line_three):
        draw.text((x, top+16+13+2), line_three, font=font, fill=255)

    # Display image.
    display.image(image)
    display.show()

def shutdown():
    draw_reset()
    draw.text((x, top+16), 'Shutting Down...',  font=font, fill=255)
    display.image(image)
    display.show()
    time.sleep(2)
    draw_reset()
    display.show()
