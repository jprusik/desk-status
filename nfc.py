import RPi.GPIO as GPIO
from pirc522 import RFID
import robin_api
import seat_status

rdr = RFID(pin_rst=25, pin_irq=24, pin_mode=GPIO.BCM)

util = rdr.util()

active_robin_id = False
active_tag_id = False
# TODO `active_status` to be last update timestamp
active_status = False

def decimal_array_to_string(decimal_array):
  return ''.join([chr(i) for i in decimal_array])

def parseRobinId(content_block):
  try:
    tag_contents = decimal_array_to_string(content_block)
    # TODO handle this better than PoC - currently assumes payload at specific address with specific length
    parsed_tag_contents = tag_contents.split('\tT\x02en')[-1].split('þ')[0]
    return (False, parsed_tag_contents)
  except:
    return (False, '')

# TODO render feedback to display instead of print
try:
  while True:
    if not active_status:
      seat_status.update_seat()
      active_status = True

    print("Waiting for tag")
    rdr.wait_for_tag()
    (request_error, tag_type) = rdr.request()

    if not request_error:
      # workaround for known issue https://github.com/ondryaso/pi-rc522/issues/10
      rdr.request()

      print("Tag detected")
      (col_error, uid) = rdr.anticoll()

      # TODO: and active_tag_id !== uid
      if not col_error:
        set_error = util.set_tag(uid)

        if not set_error:
          # normal read will succeed without auth on NTAG215
          (read_error, content_block) = util.rfid.read(4)

          if not read_error:
              print("Data was read successfully")
              (parse_error, robin_id) = parseRobinId(content_block)

              if not parse_error:
                  print("Your Robin id is:" + robin_id)

                  if active_robin_id != robin_id:
                    active_robin_id = robin_id
                    seat_reservation = robin_api.reserve_seat(robin_id)

                  try:
                    if seat_reservation['meta']['status_code'] == 200:
                      seat_status.update_seat()
                  except:
                    pass
              else:
                  print("There was a problem getting a Robin user from that tag")

          else:
              print("There was a problem reading the tag")

          # Always stop crypto1 when done working
          rdr.stop_crypto()
    else:
      active_robin_id = None

except KeyboardInterrupt:
    print("\nExit")
    # Calls GPIO cleanup
    rdr.cleanup()
