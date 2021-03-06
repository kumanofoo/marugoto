#! /usr/bin/env python3

# reference
# http://www.leancrew.com/all-this/2012/10/matplotlib-and-the-dark-sky-api/

import os
import sys
from datetime import datetime
import json
import requests

class weather:
    """
    fetch weather forecast from Dark Sky
    """
    def __init__(self):
        self.weather = ''
        
        MY_PLACE = os.environ.get("MY_PLACE")
        if not MY_PLACE:
            sys.stderr.write('no environment variable MY_PLACE\n')
            exit(1)
        else:
            self.lat, self.lon = MY_PLACE.split(':')

        self.api_key = os.environ.get("DARK_SKY_KEY")
        if not self.api_key:
            sys.stderr.write('no environment variable DARK_SKY_KEY\n')
            exit(1)

        self.weather = ''



    def fetch(self):
        url = 'https://api.darksky.net/forecast/%s/%s,%s?units=auto' % (self.api_key, self.lat, self.lon)
        resp = requests.get(url)
        if resp.status_code == 200:
            self.weather = json.loads(resp.text)
        else:
            sys.stderr.write("Connection failure to %s\n" % url)
            exit(1)

        # APIs https://darksky.net/dev/docs
        #timezone = weather['timezone']


        
    def lowest(self):
        if self.weather == '':
            self.fetch()

        low = self.weather['daily']['data'][0]['temperatureLow']
        lowTime = self.weather['daily']['data'][0]['temperatureLowTime']
        lowTimeStr = datetime.fromtimestamp(lowTime)

        return low, lowTimeStr



    def highest(self):
        if self.weather == '':
            self.fetch()

        high = self.weather['daily']['data'][0]['temperatureHigh']
        highTime = self.weather['daily']['data'][0]['temperatureHighTime']
        highTimeStr = datetime.fromtimestamp(highTime)

        return high, highTimeStr



    def summary(self):
        if self.weather == '':
            self.fetch()

        summary = self.weather['daily']['summary']
        return summary




if __name__ == '__main__':
    w = weather()
    text = w.summary()
    print(text)
    
    t, tTime = w.highest()
    print('highest temperature: ', t, tTime)

    low, lowTime = w.lowest()
    print('lowest temperature: ', low, lowTime)

    if low < -3:
        print("so cold!!")
    elif low < 5:
        print("cold!!")
