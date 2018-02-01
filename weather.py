#! /usr/bin/env python3

# reference
# http://www.leancrew.com/all-this/2012/10/matplotlib-and-the-dark-sky-api/

import os
import sys
from datetime import datetime
import json
import requests

# global variable
lowest_temp = 9999.0
lowest_temp_time = ""
highest_temp = 9999.0
highest_temp_time = ""
weather = ""
summary = ""


def fetch():
    """
    fetch forecast
    """
    global lowest_temp
    global lowest_temp_time
    global highest_temp
    global highest_temp_time
    global weather
    global summary
    
    url = 'https://api.darksky.net/forecast/%s/%s,%s?units=auto' % (_api_key, _lat, _lon)
    resp = requests.get(url)
    if resp.status_code == 200:
        weather = json.loads(resp.text)
        lowest_temp = weather['daily']['data'][0]['temperatureLow']
        low_t = weather['daily']['data'][0]['temperatureLowTime']
        lowest_temp_time = datetime.fromtimestamp(low_t)
        highest_temp = weather['daily']['data'][0]['temperatureHigh']
        high_t = weather['daily']['data'][0]['temperatureHighTime']
        highest_temp_time = datetime.fromtimestamp(high_t)
        summary = weather['daily']['summary']
    else:
        sys.stderr.write("Connection failure to %s\n" % url)
        exit(1)

    # APIs https://darksky.net/dev/docs
    #timezone = weather['timezone']



_lat = ''
_lon = ''
MY_PLACE = os.environ.get("MY_PLACE")
if not MY_PLACE:
    sys.stderr.write('no environment variable MY_PLACE\n')
    exit(1)
else:
    _lat, _lon = MY_PLACE.split(':')

_api_key = os.environ.get("DARK_SKY_KEY")
if not _api_key:
    sys.stderr.write('no environment variable DARK_SKY_KEY\n')
    exit(1)
fetch()



if __name__ == '__main__':
    print(summary)
    print('highest temperature: ', highest_temp, highest_temp_time)
    print('lowest temperature: ', lowest_temp, lowest_temp_time)

    if lowest_temp < -3:
        print("so cold!!")
    elif lowest_temp < 5:
        print("cold!!")
