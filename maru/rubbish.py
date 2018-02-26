#! /usr/bin/env python
# -*- coding: utf-8 -*-

import sys
import datetime
import json
import re

try:
    rubbish_day_file = 'rubbishday.json'
    json_db = open(rubbish_day_file, 'r')
    rubbish_day = json.load(json_db)
    json_db.close()
except Exception as e:
    sys.stderr.write("{0}\n".format(e))
    sys.stderr.write("can not open '{0}'\n".format(rubbish_day_file))
    exit(-1)
    
try:
    rubbish_lang_file = 'rubbishday_lang.json'
    json_db = open(rubbish_lang_file, 'r')
    rubbish_lang = json.load(json_db)
    ja = rubbish_lang['ja']
    json_db.close()
except Exception as e:
    sys.stderr.write("{0}\n".format(e))
    sys.stderr.write("can not open '{0}'\n".format(rubbish_lang_file))
    exit(-1)

    
def kind_of_rubbish(date):
    weekday = date.strftime('%a')
    day = int(date.strftime('%d'))
    nth = str(int(day / 7 + 1))
    return rubbish_day[weekday][nth]

if __name__ == '__main__':
    if len(sys.argv) > 1:
        date_str = sys.argv[1]
        if not re.search('^\d\d\d\d\d\d\d\d$', date_str):
            print("usage: rubbish.py [YYYYMMDD]");
            exit(-1)
        date = datetime.datetime.strptime(date_str, "%Y%m%d")
        message = date.strftime("%-m月%-d日")
    else:
        date = datetime.datetime.now()
        hour = int(date.strftime('%H'))
        if hour > 9:
            date += datetime.timedelta(days=1)
            message = '明日'
        else:
            message = '今日'
    
    rub = kind_of_rubbish(date)
    if rub:
        n = 0
        message += 'は'
        for r in rub:
            if n > 0:
                message += 'と'
            message += ja[r]
            n += 1
        message += 'の収集の日です'
    else:
        message += 'の収集はありません'
    print(message)

    #json_file = open('rubbishday.json', 'w')
    #json.dump(rubbishday, json_file, indent=2)
