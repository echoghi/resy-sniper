import requests
import time
import urllib.parse
from datetime import datetime

from log_utils import log_error, log_success, log_info
from utils import get_headers, format_slot


# Venue Configuration
VENUE_ID = 984
PARTY_SIZE = 2
DAY = "2024-05-31"


def check_availability():
    headers = get_headers()

    params = {
        'lat': '0',
        'long': '0',
        'day': DAY,
        'party_size': PARTY_SIZE,
        'venue_id': VENUE_ID
    }

    url = f'https://api.resy.com/4/find'
    encoded_params = urllib.parse.urlencode(params)
    full_url = f"{url}?{encoded_params}"

    response = requests.get(full_url, headers=headers)

    if response.status_code != 200:
        log_error(f"Failed to fetch data: {response.status_code}")
        log_error(f"Response Body: {response.text}")
        return None

    data = response.json()

    matching_slots = []

    for venue in data['results']['venues']:
        if venue['venue']['id']['resy'] == VENUE_ID:
            for slot in venue['slots']:
                if (slot['availability']['id'] == 3 and
                    '20:00:00' >= slot['date']['start'][-8:] >= '18:00:00' and
                        slot['payment']['deposit_fee'] is None):
                    matching_slots.append(slot)

    # Sort the list of matching slots by start time
    matching_slots.sort(key=lambda x: x['date']['start'])

    # Filter for preferred time range
    preferred_slots = [slot for slot in matching_slots if '19:00:00' <=
                       slot['date']['start'][-8:] <= '19:30:00']

    # Return the best available slot based on the time preference
    if preferred_slots:
        log_success("Best slot within preferred time range found:",
                    format_slot(preferred_slots[0]))
        return book_reservation(preferred_slots[0])
    elif matching_slots:
        log_success("No preferred slots found, earliest matching slot:",
                    format_slot(matching_slots[0]))
        return book_reservation(matching_slots[0])
    else:
        log_error("No matching slots found.")
        return None


def get_reservation_details(config_id):
    url = "https://api.resy.com/3/details"
    headers = get_headers({
        'X-Origin': 'https://widgets.resy.com',
        'Origin': 'https://widgets.resy.com',
        'Referer': 'https://widgets.resy.com',
        "Content-Type": "application/json",
    })

    body = {
        "config_id": config_id,
        "day": DAY,
        "party_size": PARTY_SIZE
    }
    response = requests.post(url, headers=headers, json=body)
    if response.status_code == 200:
        return response.json()
    else:
        log_error(
            f"Failed to fetch reservation details: {response.status_code}")
        return None


def book_reservation(slot):
    details = get_reservation_details(slot['config']['token'])
    if not details:
        return "Failed to get reservation details"

    payment_method_id = details.user.payment_methods[0].id
    book_token = details.book_token.value

    # URL and headers setup for booking reservation
    url = "https://api.resy.com/3/book"
    headers = get_headers({
        "Content-Type": "application/x-www-form-urlencoded",
        "X-Origin": "https://widgets.resy.com",
        "Referer": "https://widgets.resy.com/",
    })
    # Form data for the POST request
    data = {
        "book_token": book_token,
        "struct_payment_method": json.dumps({"id": payment_method_id}),
        "source_id": "resy.com-venue-details"
    }
    # Use urllib to encode the form data
    encoded_data = urllib.parse.urlencode(data)

    response = requests.post(url, headers=headers, data=encoded_data)
    if response.status_code == 200:
        return response.json()
    else:
        log_error(f"Failed to book reservation: {response.status_code}")
        return response.text


# Schedule the task to run every 15 seconds
while True:
    current_date = datetime.now().strftime('%Y-%m-%d')
    if current_date >= DAY:
        log_info("Date has passed, stopping the search.")
        break
    check_availability()
    time.sleep(15)
