import pandas as pd
from lyrics_function import get_genres, get_missing_genres
from lyrics_function import get_song_lyrics
import pandas as pd
import os
import unicodedata
from tqdm import tqdm

GENIUS_API_TOKEN = '8E4NGMZM8KOloJtNlWp8oMjHJtbuAGa07QF-VgjvGzJkEi7l-uUvLI8A4DvhKnuX'

#====================================#
#  CLEANING & FORMATTIING FUNCTIONS  #
#====================================#


def strip_accents(text):
    '''replaces characters with accents with utf-8 characters'''
    text = unicodedata.normalize('NFD', text)\
        .encode('ascii', 'ignore')\
        .decode("utf-8")
    return text


def format_track(df, col='track', new_col_name="genius_track"):
    '''formats the track columns to contain track names 
    in a genius API compliant format'''
    # replaces accented character strings with utf-8 characters
    df[new_col_name] = df[col].apply(strip_accents)
    # removes character strings inside parentheses
    df[new_col_name] = df[new_col_name].str.replace(r"\([^()]*\)", '')
    # removes any string after a hyphen
    df[new_col_name] = df[new_col_name].str.replace(r"\-.*", '')
    # removes any punctuation
    df[new_col_name] = df[new_col_name].str.replace(r'[^\w\s]', '')
    # removes any spaces at the beginning or end of strings
    df[new_col_name] = df[new_col_name].str.strip()
    # only keeps the first letter in the string capitalized -- rest are lowercased
    df[new_col_name] = df[new_col_name].str.capitalize()
    return df


def format_artist(df, col='artist', new_col_name="genius_artist"):
    '''formats the artist columns to contain only the first artists name
    in a genius API compliant format'''
    # replaces accented character strings with utf-8 characters
    df[new_col_name] = df[col].apply(strip_accents)
    # removes character strings inside parentheses
    df[new_col_name] = df[new_col_name].str.replace(r"\([^()]*\)", '')
    # removes any string after a hyphen
    df[new_col_name] = df[new_col_name].str.replace(r"\-.*", '')
    # splits into a list if there is more than one artist
    df[new_col_name] = df[new_col_name].str.split(",").str[0]
    df[new_col_name] = df[new_col_name].str.strip()
    # removes any punctuation
    df[new_col_name] = df[new_col_name].str.replace(r'[^\w\s]', '')
    # only keeps the first letter in the string capitalized -- rest are lowercased
    df[new_col_name] = df[new_col_name].str.capitalize()
    return df

#====================================#
#    Getting Lyrics from Top Songs   #
#====================================#


# import from lyrics_functions file

#====================================#
#       Putting It All Together      #
#====================================#

# getting all of the weekly data into one big data frame
df = pd.DataFrame()
files = os.listdir('cleaned_data')
for idx, file in enumerate(files):
    year = files[idx][:4]
    path = os.path.join('raw_scrape_data', file)
    dt = pd.read_csv(path)
    df = pd.concat([df, dt])

# subsetting only the global songs
global_df = df[df['country_chart'].str.contains("Global")]
top_tracks_artists = global_df.drop_duplicates(subset=['track', 'artist'])[
    ['artist', 'track']].reset_index(drop=True).dropna()

# apply format_string to artists and to track list
format_artist(top_tracks_artists)
format_track(top_tracks_artists)

# create list of song titles and artist names
song_title = top_tracks_artists.genius_track.to_list()
artist_name = top_tracks_artists.genius_artist.to_list()
song_data_lists = [list(a) for a in zip(song_title, artist_name)]
lyrics = []
for song_data in tqdm(song_data_lists):
    print("Getting Lyrics for ", song_data[0], " by ", song_data[1])
    song_lyric = get_song_lyrics(song_data[0], song_data[1])
    lyrics.append(song_lyric)
top_tracks_artists['lyrics'] = lyrics
top_tracks_artists.to_csv(
    'cleaned_data/all_top_songs_with_lyrics.csv', index=False)

# DATA CLEANING

df = pd.read_csv(
    '/Users/daphneyang/Desktop/5YMIDS_SP21/w209/spotify-visualizations/cleaned_data/all_top_songs_with_lyrics.csv')
track = df['genius_track'].to_list()
artist = df['genius_artist'].to_list()
zipped = [list(a) for a in zip(track, artist)]
genres = []
for song in tqdm(zipped):
    print("getting genre for", song[0], " by ", song[1])
    genre = get_genres(song[0], song[1])
    if genre == "missing genre":
        genre = get_missing_genres(song[0], song[1])
    genres.append(genre)
# split the lists
split_genres = [str(i[0]).replace('tag:', "").split(",") for i in genres]

df_ = df.copy()
# add to dataframe and clean the values
df_['genre'] = split_genres
df_['genre'] = df_.genre.astype(str).str.replace('[', '')
df_['genre'] = df_.genre.astype(str).str.replace(']', '')
df_['genre'] = df_.genre.astype(str).str.replace("'", '')
