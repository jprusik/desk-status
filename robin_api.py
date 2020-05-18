from datetime import datetime
from dateutil import tz
import json
import requests
import os
from os.path import join, dirname
from dotenv import load_dotenv

# Create .env file path.
dotenv_path = join(dirname(__file__), '.env')

# Load file from the path.
load_dotenv(dotenv_path)

API_ACCESS_TOKEN = os.getenv('API_ACCESS_TOKEN')
API_DOMAIN_URL = os.getenv('API_DOMAIN_URL')
SEAT_ID = os.getenv('SEAT_ID')
ORG_ID = os.getenv('ORG_ID')
TIMEZONE_STRING = os.getenv('TIMEZONE_STRING')

headers = {
    'Content-Type': 'application/json;charset=utf-8',
    'Authorization': 'Access-Token' + API_ACCESS_TOKEN,
    'Tenant-Id': str(ORG_ID)
}

# TODO when desk `get_robin_desk` is called, update reserve_type
desk_reserve_type = 'assigned'

def rest_of_the_day():
    now = datetime.now()
    end = now.replace(hour=23, minute=59, second=59, microsecond=59)
    return now, end

def reserve_seat(user_id):
    try:
        (now, end) = rest_of_the_day()

        payload = {
            'type': desk_reserve_type,
            'start': {
                'date_time': now.astimezone().replace(microsecond=0).isoformat(),
                'time_zone': TIMEZONE_STRING
            },
            'end': {
                'date_time': end.astimezone().replace(microsecond=0).isoformat(),
                'time_zone': TIMEZONE_STRING
            },
            'reservee': {
                'user_id': user_id
            },
            'reserver_id': user_id
        }

        response = requests.post('https://'+API_DOMAIN_URL+'/v1.0/seats/'+SEAT_ID+'/reservations', json=payload, headers=headers, params={"access_token": API_ACCESS_TOKEN})

        return response.json()
    except:
        print('request errored')
        return json.loads('{"data":[]}')

def get_reservees_by_seat():
    url = 'https://'+API_DOMAIN_URL+'/v1.0/seats/'+SEAT_ID+'/reservations'

    try:
        now = datetime.now().astimezone().replace(microsecond=0).isoformat()
        params = {
            'access_token': API_ACCESS_TOKEN,
            'after': now,
            'include': 'seat,seat.zone,seat.zone,reservee.user'
        }
        response = requests.get(url, headers=headers, params=params)

        return response.json()
    except:
        return json.loads('{"data":[]}')

def get_seat():
    url = 'https://'+API_DOMAIN_URL+'/v1.0/seats/'+SEAT_ID

    try:
        params = {'access_token': API_ACCESS_TOKEN, 'include': 'zone'}
        response = requests.get(url, params=params)

        return response.json()
    except:
        return json.loads('{"data": {}}')
