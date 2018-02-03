#! /usr/bin/env python

import os
import re
import sys
import json
import shutil
from datetime import datetime
import argparse

import requests
from bs4 import BeautifulSoup


WEEKDAY = {'weekday':0, 'saturday':1, 'sunday':2}

def parse_navitime(soup, bus_line):
    time_table = {}

    for wds, wdv in WEEKDAY.items():
        time_table[wds] = []
        div = soup.find_all("div", class_="diagramTable", id=bus_line+'_'+str(wdv))
        for div_i in div:
            dl = div_i.find_all("dl", class_=re.compile("dl_\d"))
            for dl_i in dl:
                dt = dl_i.find_all("dt")
                hour = dt[0].string
                div2 = dl_i.find_all("div", style=re.compile("underline"))
                for div2_i in div2:
                    time_table[wds].append(int(hour + div2_i.string))
    return time_table


def fetch(time_table_json='time_table.json'):
    time_table = {}
    for wds in WEEKDAY.keys():
        time_table[wds] = []

    URL = os.environ.get('NAVI_TIME')
    if not URL:
        sys.stderr.write("no environment variable NAVI_TIME\n");
        exit(0)

    LINES = os.environ.get('NAVI_TIME_LINES')
    if not LINES:
        sys.stderr.write("no environment variable NAVI_TIME_LINES\n");
        exit(0)

    lines = LINES.split(':')
    for line in lines:
        url = URL + line + '/'
        resp = requests.get(url)
        if resp.status_code != 200:
            sys.stderr.write("can not fetch time table\n")
            exit(0)
        soup = BeautifulSoup(resp.text, "lxml")
        line_key = 'd_' + str((line.split('/'))[1])
        tt = parse_navitime(soup, line_key)
        for wds, wdv in tt.items():
            time_table[wds].extend(wdv)

    if os.path.exists(time_table_json):
        backup_file = time_table_json + '.bak'
        shutil.copyfile(time_table_json, backup_file)

    json_file = open(time_table_json, 'w')
    json.dump(time_table, json_file, indent=2, sort_keys=True)

            

def get_next_bus(time_table_json='time_table.json', remaining=False):
    try:
        json_db = open(time_table_json, 'r')
        time_table = json.load(json_db)
        json_db.close()
    except Exception as e:
        sys.stderr.write("{0}\n".format(e))
        sys.stderr.write("can not open '{0}'\n".format(time_table_json))
        sys.stderr.write("(use \"bus.py -f\")\n")
        exit(0)

    now = datetime.now()
    wday = now.strftime('%a')
    if wday == 'Sat':
        key = 'saturday'
    elif wday == 'Sun':
        key = 'sunday'
    else:
        key = 'weekday'

    time_s = now.strftime('%H%M')
    time = int(time_s)

    first = []
    i = 99999
    sorted_tab = sorted(time_table[key])
    for t in sorted_tab:
        if t > time+5: # +5 min
            first.append(str(t))
            i = sorted_tab.index(t)
            break

    if i+1 < len(sorted_tab):
        first.append(str(sorted_tab[i+1]))
    if i+2 < len(sorted_tab):
        first.append(str(sorted_tab[i+2]))

    res = []
    if remaining:
        dt_now = datetime.strptime(time_s, "%H%M")
        for f in first:
            dt = datetime.strptime(f, "%H%M")
            delta_min = int((dt-dt_now).total_seconds()/60)
            res.append(delta_min)
    else:
        res  = list(map(int, first))

    return res



if __name__ == '__main__':
    parser = argparse.ArgumentParser()
    parser.add_argument("-r", "--remaining",
                        help="display remaining times",
                        action="store_true")
    parser.add_argument("-f", "--fetch",
                        help="fetch time table and save",
                        action="store_true")
    parser.add_argument("-t", "--time-table-file",
                        help="time table file (JSON)",
                        action="store",
                        type=str,
                        default='time_table.json')
    args = parser.parse_args()

    if args.fetch:
        fetch(args.time_table_file)

    next_bus = get_next_bus(time_table_json=args.time_table_file,
                            remaining=args.remaining)
    for nb in next_bus:
        print(nb)
