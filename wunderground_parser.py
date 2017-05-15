from datetime import datetime, timedelta
from bs4 import BeautifulSoup
from urllib2 import urlopen


def parse_station(station):
    '''
    This function parses the web pages downloaded from wunderground.com
    into a flat CSV file for the station you provide it.

    Make sure to run the wunderground scraper first so you have the web
    pages downloaded.
    '''

    # Scrape between Oct 1, 2016 and Oct 31, 2016
    # You can change the dates here if you prefer to parse a different range
    current_date = datetime(year=2016, month=10, day=01)
    end_date = datetime(year=2016, month=10, day=31)

    with open('{}.csv'.format(station), 'w') as out_file:
        out_file.write('date,actual_min_temp,actual_max_temp,'
                            'average_min_temp,average_max_temp\n')

        while current_date != end_date:
            try_again = False
            with open('{}/{}-{}-{}.html'.format(station,
                                                current_date.year,
                                                current_date.month,
                                                current_date.day)) as in_file:
                soup = BeautifulSoup(in_file.read(), 'html.parser')

                weather_data = soup.find(id='historyTable').find_all('span', class_='wx-value')
                weather_data_units = soup.find(id='historyTable').find_all('td')

                try:
                    actual_max_temp = weather_data[1].text
                    average_max_temp = weather_data[2].text
                    actual_min_temp = weather_data[4].text
                    average_min_temp = weather_data[5].text

                    out_file.write('{}-{}-{},'.format(current_date.year, current_date.month, current_date.day))
                    out_file.write(','.join([actual_min_temp, actual_max_temp,
                                            average_min_temp, average_max_temp]))
                    out_file.write('\n')
                    current_date += timedelta(days=1)
                except:
                    # If the web page is formatted improperly, signal that the page may need
                    # to be downloaded again.
                    try_again = True

            # If the web page needs to be downloaded again, re-download it from
            # wunderground.com

            # If the parser gets stuck on a certain date, you may need to investigate
            # the page to find out what is going on. Sometimes data is missing, in
            # which case the parser will get stuck. You can manually put in the data
            # yourself in that case, or just tell the parser to skip this day.
            if try_again:
                print('Error with date {}'.format(current_date))

                lookup_URL = 'http://www.wunderground.com/history/airport/{}/{}/{}/{}/DailyHistory.html'
                formatted_lookup_URL = lookup_URL.format(station,
                                                         current_date.year,
                                                         current_date.month,
                                                         current_date.day)
                html = urlopen(formatted_lookup_URL).read().decode('utf-8')

                out_file_name = '{}/{}-{}-{}.html'.format(station,
                                                          current_date.year,
                                                          current_date.month,
                                                          current_date.day)

                with open(out_file_name, 'w') as out_file:
                    out_file.write(html)


# Parse the stations
for station in ['RKSS']:
    parse_station(station)