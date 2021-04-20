import requests
from bs4 import BeautifulSoup
from regex import search
import regex as re
import unicodedata
from tqdm import tqdm

base_url = "http://api.genius.com"
headers = {
    'Authorization': 'Bearer QVcv1b9UiW5yvCxJ27nwWvwXvhlFO24BbztO6FMosdpOIeTHfFfJ_Gr7Wq6C_Qep'}


def strip_accents(text):
    '''replaces characters with accents with utf-8 characters'''
    text = unicodedata.normalize('NFD', text)\
        .encode('ascii', 'ignore')\
        .decode("utf-8")
    return text

#====================================#
#           Lyrics Functions         #
#====================================#


def lyrics_from_song_api_path(song_api_path):
    song_url = base_url + song_api_path
    response = requests.get(song_url, headers=headers)
    song_response = response.json()
    path = song_response["response"]["song"]["path"]
    page_url = "http://genius.com" + path
    page = requests.get(page_url)
    html = BeautifulSoup(page.text, "html.parser")
    # removes script tags that they put in the middle of the lyrics
    [h.extract() for h in html('script')]
    lyrics = html.find("div", class_="lyrics").get_text()
    return lyrics


def get_missing(song_title, artist_name):
    """ Helper Function for best effort flexible matching for missing lyrics """
    search_string = f'{song_title} by {artist_name}'.replace(' ', "%20")
    search_url = base_url + "/search?q=" + search_string
    response = requests.get(search_url, headers=headers)
    json = response.json()
    song_info = None
    for hit in json["response"]["hits"]:
        genius_artist_result = strip_accents(
            hit["result"]["primary_artist"]["name"]).lower()
        if search(artist_name.lower(), genius_artist_result):
            song_info = hit
            break
    if song_info:
        song_api_path = song_info["result"]["api_path"]
        lyrics = lyrics_from_song_api_path(song_api_path)
        # Removes new-line characters
        # splits = lyrics.split('/n')
        # lyrics = ". ".join(splits)
        lyrics = lyrics.replace('\n', " ")
        # Removes any parentheses or [] bound strings
        lyrics = re.sub(r"([\(\[]).*?([\)\]])", '', lyrics)
        lyrics = lyrics.replace(']', "")
        return lyrics
    else:
        return "missing lyrics"


def get_song_lyrics(song_title, artist_name):
    search_url = base_url + "/search?"
    data = {'q': song_title}
    response = requests.get(search_url, params=data, headers=headers)
    json = response.json()
    song_info = None
    for hit in json["response"]["hits"]:
        genius_artist_result = hit["result"]["primary_artist"]["name"].lower()
        if search(artist_name.lower(), genius_artist_result):
            song_info = hit
            break
    if song_info:
        song_api_path = song_info["result"]["api_path"]
        lyrics = lyrics_from_song_api_path(song_api_path)
        # Removes new-line characters
        # splits = lyrics.split('/n')
        # lyrics = ". ".join(splits)
        lyrics = lyrics.replace('\n', " ")
        # Removes any parentheses or [] bound strings
        lyrics = re.sub(r"([\(\[]).*?([\)\]])", '', lyrics)
        lyrics = lyrics.replace(']', "")
        return lyrics
    else:
        return get_missing(song_title, artist_name)

#====================================#
#           Genre Functions          #
#====================================#


def get_genres(song_title, artist_name):

    search_string = f'{song_title} by {artist_name}'.replace(' ', "%20")
    search_url = base_url + "/search?q=" + search_string
    response = requests.get(search_url, headers=headers)

    json = response.json()
    song_info = None
    for hit in json["response"]["hits"]:
        genius_artist_result = strip_accents(
            hit["result"]["primary_artist"]["name"]).lower()
        if search(artist_name.lower(), genius_artist_result):
            song_info = hit
            break
    if song_info:
        song_api_path = song_info["result"]["api_path"]

        song_url = base_url + song_api_path
        response = requests.get(song_url, headers=headers)
        song_response = response.json()
        path = song_response["response"]["song"]["path"]
        page_url = "http://genius.com" + path
        page = requests.get(page_url)
        html = BeautifulSoup(page.text, "html.parser")
        string = html.findAll('script')
        genre_raw_data = re.findall(r"tag:(.*?)'", str(string))
        return genre_raw_data
    else:
        return 'missing genre'


def get_missing_genres(song_title, artist_name):

    search_url = base_url + "/search?"
    data = {'q': song_title}
    response = requests.get(search_url, params=data, headers=headers)

    json = response.json()
    song_info = None
    for hit in json["response"]["hits"]:
        genius_artist_result = strip_accents(
            hit["result"]["primary_artist"]["name"]).lower()
        if search(artist_name.lower(), genius_artist_result):
            song_info = hit
            break
    if song_info:
        song_api_path = song_info["result"]["api_path"]

        song_url = base_url + song_api_path
        response = requests.get(song_url, headers=headers)
        song_response = response.json()
        path = song_response["response"]["song"]["path"]
        page_url = "http://genius.com" + path
        page = requests.get(page_url)
        html = BeautifulSoup(page.text, "html.parser")
        string = html.findAll('script')
        genre_raw_data = re.findall(r"tag:(.*?)'", str(string))
        return genre_raw_data
    else:
        return 'missing genre'
