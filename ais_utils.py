#module import
import urllib.request
from bs4 import BeautifulSoup
import re
import pandas as pd
from datetime import datetime
#import locale
#locale.setlocale(locale.LC_ALL, 'en_US') #as we need to deal with names of monthes later on.
import os

def substring_after(s, delim):
    return s.partition(delim)[2]

def get_ship_lat_lon(IMO: float = 9327774):
    hdr = {'User-Agent': 'Mozilla/5.0 (X11; Linux x86_64) AppleWebKit/537.11 (KHTML, like Gecko) Chrome/23.0.1271.64 Safari/537.11',
           'Accept': 'text/html,application/xhtml+xml,application/xml;q=0.9,*/*;q=0.8',
           'Accept-Charset': 'ISO-8859-1,utf-8;q=0.7,*;q=0.3',
           'Accept-Encoding': 'none',
           'Accept-Language': 'en-US,en;q=0.8',
           'Connection': 'keep-alive'}

    url = r'https://www.vesselfinder.com/en/vessels/VOS-TRAVELLER-IMO-' + \
        str(IMO)
    req = urllib.request.Request(url, None, hdr)
    with urllib.request.urlopen(req) as response:
        the_page = response.read()
    parsed_html = BeautifulSoup(the_page)
    #parsed_html.find_all("")
    for paragraph in parsed_html.find_all('p'):
        p = str(paragraph.text)
        if 'coordinates' in p:
            text_after = substring_after(p, 'coordinates ')
            lat = float(text_after[0:8])
            lat_card = text_after[9]
            lon = float(text_after[13:21])
            lon_card = text_after[22]

    return lat, lat_card, lon, lon_card

def get_gc1205_lat_lon():
    hdr = {'User-Agent': 'Mozilla/5.0 (X11; Linux x86_64) AppleWebKit/537.11 (KHTML, like Gecko) Chrome/23.0.1271.64 Safari/537.11',
           'Accept': 'text/html,application/xhtml+xml,application/xml;q=0.9,*/*;q=0.8',
           'Accept-Charset': 'ISO-8859-1,utf-8;q=0.7,*;q=0.3',
           'Accept-Encoding': 'none',
           'Accept-Language': 'en-US,en;q=0.8',
           'Connection': 'keep-alive'}

    url = r'https://www.vesselfinder.com/fr/vessels/CCG-C03615QC-IMO-0-MMSI-316010216'
    req = urllib.request.Request(url, None, hdr)
    with urllib.request.urlopen(req) as response:
        the_page = response.read()
    parsed_html = BeautifulSoup(the_page, features="html.parser")
    #parsed_html.find_all("")

    ongoing = True
    lat, lon = None, None
    for paragraph in parsed_html.find_all(True):
        if ongoing:
            p = str(paragraph.text)
            if "Lat" in p:
                lat_str = substring_after(p, 'Lat')
                if lat is None:
                    try:
                        lat = float(lat_str[1:9])
                    except:
                        pass
            if "Lon" in p:
                lon_str = substring_after(p, 'Lon')
                if lon is None:
                    try:
                        lon = float(lon_str[1:10])
                    except:
                        pass

    return lat, lon
