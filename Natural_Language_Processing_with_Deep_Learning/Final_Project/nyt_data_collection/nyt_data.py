import json
import requests
import os
import time
import datetime
import dateutil
import pandas as pd
from dateutil.relativedelta import relativedelta
from newspaper import Article

# Git LFS Accessing Files: on CLI ->gi
# git lfs pull --include="nyt_data_collection/dataset/train_dataset.csv"


# def get_article(year, month):
#     url = f'https://api.nytimes.com/svc/archive/v1/{year}/{month}.json?&api-key=7nGJF34cDaTiWtnOAXWYs5NR3iUIZQPU'
#     return url
# session = requests.Session()

# headers = {'User-Agent': 'Mozilla/5.0 (Windows NT 6.1; WOW64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/56.0.2924.76 Safari/537.36'} # This is chrome, you can set whatever browser you like

# response = requests.get(get_article(2021,1), headers = headers)
# nyt = json.loads(response.text)
# nyt.keys()

end = datetime.date.today()
start = end - relativedelta(years=5)
months_in_range = [x.split(' ') for x in pd.date_range(
    start, end, freq='MS').strftime("%Y %-m").tolist()]
months_in_range


def send_request(date):
    '''Sends a request to the NYT Archive API for given date.'''
    base_url = 'https://api.nytimes.com/svc/archive/v1/'
    url = base_url + '/' + date[0] + '/' + date[1] + \
        '.json?api-key=7nGJF34cDaTiWtnOAXWYs5NR3iUIZQPU'
    response = requests.get(url).json()
    time.sleep(6)
    return response


def is_valid(article, date):
    '''An article is only worth checking if it is in range, and has a headline.'''
    is_in_range = date > start and date < end
    has_headline = type(
        article['headline']) == dict and 'main' in article['headline'].keys()
    return is_in_range and has_headline


def get_metadata(response):
    '''Parses and returns response as pandas data frame.'''
    data = {'headline': [],
            'date': [],
            'doc_type': [],
            'material_type': [],
            'section': [],
            'abstract': [],
            'first_paragraph': [],
            'keywords': [],
            'web_url': []}

    articles = response['response']['docs']
    for article in articles:  # For each article, make sure it falls within our date range
        date = dateutil.parser.parse(article['pub_date']).date()
        if is_valid(article, date):
            data['date'].append(date)
            data['headline'].append(article['headline']['main'])
            data['abstract'].append(article['abstract'])
            data['first_paragraph'].append(article['lead_paragraph'])
            data['web_url'].append(article['web_url'])
            if 'section' in article:
                data['section'].append(article['section_name'])
            else:
                data['section'].append(None)
            data['doc_type'].append(article['document_type'])
            if 'type_of_material' in article:
                data['material_type'].append(article['type_of_material'])
            else:
                data['material_type'].append(None)
            keywords = [keyword['value']
                        for keyword in article['keywords'] if keyword['name'] == 'subject']
            data['keywords'].append(keywords)
    return pd.DataFrame(data)


# def get_article(metadata_df):
#     article_text = []
#     for article_url in metadata_df['web_url'].to_list():
#         if len(article_url) > 0:
#             # if there is a article link, extract all article text
#             article = Article(article_url)
#             article.download()
#             article.html
#             article.parse()
#             article_text.append(article.text)
#         else:
#             article_text.append('none')
#     metadata_df['article_text'] = article_text
#     return metadata_df


def get_data(dates):
    '''Sends and parses request/response to/from NYT Archive API for given dates.'''
    total = 0
    print('Date range: ' + str(dates[0]) + ' to ' + str(dates[-1]))
    if not os.path.exists('headlines'):
        os.mkdir('headlines')
    for date in dates:
        response = send_request(date)
        df = get_metadata(response)
        df_news = df.loc[(df["doc_type"] == 'article') &
                         (df['material_type'] == 'News')]
        # df_text = get_article(df)
        # total += len(df_text)
        total += len(df_news)
        df_news.to_csv(
            'headlines/' + date[0] + '-' + date[1] + '.csv', index=False)
        print('Saving headlines/' + date[0] + '-' + date[1] + '.csv...')
    print('Number of articles collected: ' + str(total))


get_data(months_in_range)
