from gpiozero import RGBLED
from colorzero import Color
import os
from os.path import join, dirname
from dotenv import load_dotenv

# Create .env file path.
dotenv_path = join(dirname(__file__), '.env')

# Load file from the path.
load_dotenv(dotenv_path)

RED_GPIO = os.getenv('RED_GPIO')
GREEN_GPIO = os.getenv('GREEN_GPIO')
BLUE_GPIO = os.getenv('BLUE_GPIO')

led = RGBLED(red=RED_GPIO, green=GREEN_GPIO, blue=BLUE_GPIO)

def signal_location():
    original_color = led.color
    pulse_count = 4
    pulse_color = Color('yellow')
    pulse_fade_duration = 0.5
    led.pulse(pulse_fade_duration, pulse_fade_duration, pulse_color, (0,0,0), pulse_count, False)
    led.color = original_color

def signal_service_needed():
    original_color = led.color
    pulse_count = 5
    pulse_color = Color('red')
    pulse_fade_duration = 0.1
    led.pulse(pulse_fade_duration, pulse_fade_duration, pulse_color, (0,0,0), pulse_count, False)
    led.color = original_color

def set_status(status):
    if status == 'AVAILABLE':
        led.color = Color('green')
    elif status == 'UNAVAILABLE':
        led.color = Color('red')
    else:
        led.color = (0, 0, 0)
