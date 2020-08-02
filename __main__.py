import status_display

def main():
    try:
        while True:
            status_display.update_seat()
            status_display.time.sleep(int(status_display.robin_api.API_POLL_INTERVAL))

    except:
        status_display.shutdown()

main()
