import scraper_functions as scrape
import pandas as pd
import os
from tqdm import tqdm
from multiprocessing import Pool

## Scraper Inputs ##
# start_date = '2016-12-30'
# end_date = '2018-01-05'
# year = '2017'
# start_date = '2018-01-05'
# end_date = '2019-01-04'
# year = '2018'
start_date = '2019-01-04'
end_date = '2020-01-03'
year = '2019'
## File Paths ##
root_path = "raw_scrape_data"

# check to see if the scrape_data dir exists -- if not, create one 
if not os.path.exists(root_path):
    os.makedirs(root_path)


loc_code, loc_name = scrape.get_locations()
dates = scrape.list_dates(start_date, end_date)

## all data cumulates
df = pd.DataFrame()
for date in tqdm(dates):
    for i in tqdm(range(len(loc_code))):
        loc_link = scrape.get_chart_url(loc_code[i], "weekly", date[0],date[1])
        chart_df = scrape.scrape_spotify(loc_link, loc_name[i], date[0])
        df = pd.concat([df, chart_df])
scrape.output(df, year)



