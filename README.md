# Desk Status Display and Check-in

This project aims to create an accessible desk-oriented status and check-in system at a low cost at scale. This particular implementation leverages the [Robin](https://robinpowered.com/) platform to retrieve and display desk availability information as well as (optionally) allow touch-less desk check-ins with user NFC/RFID cards/tags.

The code provided here is based on [mini-ticker](https://github.com/jprusik/mini-ticker), which in turn is based on examples from the [pi-rc522](https://github.com/ondryaso/pi-rc522) and [adafruit-circuitpython-ssd1306](https://github.com/adafruit/Adafruit_CircuitPython_SSD1306) projects.

## Requirements

- Raspberry Pi computer with installed header pins and power source
- [compatible](https://www.raspberrypi.org/documentation/installation/sd-cards.md) microSD card
- SSD1306-based 128x64 or 128x32 pixel OLED display
- (Optional) RC522 module (for RFID/NFC communication)

## Setup

- [Install Raspbian (Lite)](https://www.raspberrypi.org/downloads/raspbian/) on a microSD/SD card
- Set up the Raspberry Pi to run headless and connect it to your network ([guide](https://www.raspberrypi.org/documentation/configuration/wireless/headless.md))
- [ssh into the Raspberry Pi](https://www.raspberrypi.org/documentation/remote-access/ssh/):
- Do `sudo raspi-config` and set up:
  - "Interfacing Options" > "Interfacing Options" > "I2C" > select "Yes"
  - (Optional) "Localisation Options"
  - (Optional) "Change User Password"
    **Important!** Because we're using a Raspberry Pi, the default user is `pi` with a password of `raspberry` - it is strongly advised to change the password, at minimum.
- Install dependencies:

  ```shell
  sudo apt update && sudo apt-get install git python3-pip python3-dev libtiff5-dev libopenjp2-7-dev
  ```

- Clone this repo and `cd desk-status`
- Install required packages with `pip3 install -r requirements.txt`
- (Optional) Edit `/boot/config.txt` at the line `dtparam=i2c_arm=on` and replace it with:

  ```shell
  dtparam=i2c_arm=on,i2c_arm_baudrate=400000
  ```

- (Optional) If using an RC522 module for RFID/NFC communication, edit `/boot/config.txt` to include the following settings:

  ```settings
  device_tree_param=spi=on
  dtoverlay=spi-bcm2708
  dtparam=spi=on
  ```

Edit or create `.env` in the same directory as `seat_status.py` with the following contents:

```shell
API_ACCESS_TOKEN="AABBCCDDEEFFGG" # Your Robin API access token
API_DOMAIN_URL="api.robinpowered.com" # The domain for Robin API calls
SEAT_ID="0" # The id of the Robin desk this display is running for
ORG_ID=0 # The id of your Robin organization
TIMEZONE_STRING="America/New_York" # The desk's tz database time zone name ('e.g. America/New_York')
```

## Running the code

Once the `seat_status.py` script is executed, it will continue to run until the process is terminated. You can manually execute the script on demand, or automatically execute on shell start by editing `/etc/profile` and appending the following to the end of the file:

```shell
sudo python3 /home/pi/seat_status.py
```

## Notes

- This build assumes Raspberry Pi Zero hardware - no other Raspberry Pi hardware has been tested with this code.
- [Ubuntu Font Family](https://design.ubuntu.com/font/) is included in `/fonts` by default. If you wish to use a different font, add them to the `/fonts` directory and update the import references in `seat_status.py` (note, line spacing currently presumes Ubuntu fonts and may require adjustments when using other fonts).
- Tip: You can access the the target pi on your network using the pi's network DNS reference (`raspberrypi` by default). This is particularly useful if your network has dynamic IP address assignment; you can simply `ssh pi@raspberrypi.local`)
