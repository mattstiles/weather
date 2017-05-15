# coding: utf-8

from datetime import datetime, timedelta
from urllib2 import urlopen
import os


def scrape_station(station):

    # You can change the dates here if you prefer to scrape a different range
    current_date = datetime(year=2016, month=10, day=01)
    end_date = datetime(year=2016, month=10, day=31)

    # Make sure a directory exists for the station web pages
    os.mkdir(station)

    #our station: https://www.wunderground.com/global/stations/58367.html
    #its history: https://www.wunderground.com/history/airport/ZSSS/2016/11/03/DailyHistory.html?req_city=Shanghai&req_statename=China&reqdb.zip=00000&reqdb.magic=1&reqdb.wmo=58367

    # Use .format(station, YYYY, M, D)
    lookup_URL = 'http://www.wunderground.com/history/airport/{}/{}/{}/{}/DailyHistory.html'

    while current_date != end_date:

        if current_date.day == 1:
            print(current_date)

        formatted_lookup_URL = lookup_URL.format(station,
                                                 current_date.year,
                                                 current_date.month,
                                                 current_date.day)
        html = urlopen(formatted_lookup_URL).read().decode('utf-8')

        out_file_name = '{}/{}-{}-{}.html'.format(station, current_date.year,
                                                  current_date.month,
                                                  current_date.day)

        with open(out_file_name, 'w') as out_file:
            out_file.write(html)

        current_date += timedelta(days=1)

# Scrape the stations (Seoul = RKSS)
# Scrape the stations (Shanghai = ZSSS)
for station in ['RKSS']:
    scrape_station(station)
