from dotenv import load_dotenv
from datetime import datetime
import os

# Load environment variables from .env file
load_dotenv()

# Authentication
API_KEY = os.getenv('API_KEY')
AUTH_TOKEN = os.getenv('AUTH_TOKEN')


def get_headers(custom_headers=None):
    # Default headers
    default_headers = {
        'Authorization': f'ResyAPI api_key="{API_KEY}"',
        'X-Resy-Auth-Token': AUTH_TOKEN,
        'X-Resy-Universal-Auth': AUTH_TOKEN,
        'X-Origin': 'https://resy.com',
        'Origin': 'https://resy.com',
        'Referer': 'https://resy.com/',
        'User-Agent': 'Mozilla/5.0 (Macintosh; Intel Mac OS X 10_15_7) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/124.0.0.0 Safari/537.36',
        'Accept': 'application/json, text/plain, */*',
        'Accept-Language': 'en-US,en;q=0.6',
    }

    # Update default headers with any custom headers provided
    if custom_headers:
        default_headers.update(custom_headers)

    return default_headers


def format_slot(slot):
    # Extract the start time from the slot information
    start_time = slot['date']['start']
    # Parse the datetime string into a datetime object
    datetime_obj = datetime.strptime(start_time, '%Y-%m-%d %H:%M:%S')
    # Format the datetime object into a more readable 12-hour format with the day
    # e.g., "Friday, January 01, 2021 07:30 PM"
    formatted_time = datetime_obj.strftime('%A, %B %d, %Y %I:%M %p')
    return formatted_time
