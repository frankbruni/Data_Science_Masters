from bs4 import BeautifulSoup
import requests
from urllib.request import Request, urlopen
import pandas as pd
import datetime as dt
import os
from tqdm import tqdm
from multiprocessing import Pool

# Site follows this formatting below:
# https://spotifycharts.com/regional/global/daily/2021-02-11

def get_chart_url(country_code, interval, date1, date2):
    """Gets a url with the specified parameters"""
    chart_url = f'https://spotifycharts.com/regional/{country_code}/{interval}/{date1}--{date2}'
    return chart_url

def list_dates(start_date, end_date):
    """Gets the list of all of the dates inclusive of start and end date"""
    end = dt.datetime.strptime(end_date, "%Y-%m-%d").date()
    start = dt.datetime.strptime(start_date, "%Y-%m-%d").date()
    delta = end - start
    dates = [(start+dt.timedelta(weeks = i)).strftime('%Y-%m-%d') for i in range(delta.days//7)]
    date_pairs = []
    for i in range(len(dates)-1):
        pair = list([dates[i], dates[i+1]])
        date_pairs.append(pair)
    return date_pairs

def get_locations():
    """Gets a list of all the country codes to scrape"""
    url = requests.get('https://spotifycharts.com/regional')
    soup = BeautifulSoup(url.content, "html.parser")
    locations = soup.find('ul').find_all('li')
    location_code = [locations[i]['data-value'] for i in range(len(locations))]
    location_name = [locations[i].text for i in range(len(locations))]
    return location_code, location_name


def scrape_spotify(chart_url, country_name, date):
    """Scrapes all of the titles, artists, stream counts, spotify link, and the rank for the specified url"""
    # use the defined get_chart_url function to get the corresponding url to scrape
    urls = requests.get(chart_url)
    soup = BeautifulSoup(urls.content, "html.parser")
    # need all of the track names, line below gives you all of the info from the chart
    trackinfo = soup.find_all('td', class_ = 'chart-table-track')
    # list comp to get all the track names
    track = [trackinfo[i].strong.text for i in range(len(trackinfo))]
    # list com to get all the artist names; slicing for just the name and removing the "by"
    artist = [trackinfo[i].span.text[3:] for i in range(len(trackinfo))]
    # need all of the stream counts, getting all the relevant with the tag elements too
    stream_counts = soup.find_all('td', class_ = 'chart-table-streams')
    # list comp to get just the text for the number of streams per track
    streams = [stream_counts[i].text for i in range(len(stream_counts))]

    # href links for the songs as well
    all_song_links = soup.find_all('td', class_ = 'chart-table-image')
    spotify_link = [all_song_links[i].a.get('href') for i in range(len(all_song_links))]
    
    # put into a dataframe and include a ranking column for reference
    df = pd.DataFrame({'rank':list(range(1,len(track)+1,1)), 'artist': artist,'track': track,'streams':streams, 'spotify_link': spotify_link})
    df['country_chart'] = country_name
    df['week start date'] = date
    return df

def output(df, year):
    df.to_csv(f'./{year}_weekly_all_locations_top200.csv', index = False)


# #####################################
# ## Scraper Inputs ##
# start_date = '2020-01-01'
# end_date = '2021-02-12'

# ## File Paths ##
# root_path = "scrape_data"
# dir_2020 = os.path.join(root_path, "2020")
# dir_2021 = os.path.join(root_path, "2021")

# # check to see if the scrape_data dir exists -- if not, create one 
# if not os.path.exists(root_path):
#     os.makedirs(root_path)

# # check to see if the sub directories for the years exsits -- if not, create them 
# if not os.path.exists(dir_2020):
#     os.makedirs(dir_2020)
# if not os.path.exists(dir_2021):
#     os.makedirs(dir_2021)



# # dates = list_dates(start_date, end_date)
# # def scraper(date):
# #     df = pd.DataFrame()
#     loc_code, loc_name = get_locations()
#     for i in tqdm(range(len(loc_code))):
#         loc_link = get_chart_url(loc_code[i], "daily", date)
#         chart_df = scrape_spotify(loc_link, loc_name[i], date)
#         df = pd.concat([df, chart_df])
#     if date[:4] == '2020':
#         dir_path = dir_2020
#     else:
#         dir_path = dir_2021
#     output(df, dir_path, date)

# pool = Pool(20)
# data_outputs = pool.map(scraper, dates)
# pool.close()
# pool.join()

# # loc_code, loc_name = get_locations()
# # dates = list_dates(start_date, end_date)

# # df = pd.DataFrame()
# # for date in tqdm(dates):
# #     for i in tqdm(range(len(loc_code))):
# #         loc_link = get_chart_url(loc_code[i], "daily", date)
# #         chart_df = scrape_spotify(loc_link, loc_name[i], date)
# #         df = pd.concat([df, chart_df])
# #     if date[:4] == '2020':
# #         dir_path = dir_2020
# #     else:
# #         dir_path = dir_2021
# #     output(df, dir_path, date)