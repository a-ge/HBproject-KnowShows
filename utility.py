# Note to remember info needed
# artist id, name, website, photo, genre, bio, **song
# event id, event title, event date, event time, event url
# venue name, venue location, venue url?

# To grab keys from sh file
import os
SPOTIPY_CLIENT_ID = os.getenv('SPOTIPY_CLIENT_ID')
SPOTIPY_CLIENT_SECRET = os.getenv('SPOTIPY_CLIENT_SECRET')
CONSUMER_KEY = os.getenv('CONSUMER_KEY')

# Spotipy is a Python client library for the Spotify Web API
import spotipy
# Spotipy provides a class SpotifyClientCredentials that can be used to authenticate requests
from spotipy.oauth2 import SpotifyClientCredentials
client_credentials_manager = SpotifyClientCredentials(client_id=SPOTIPY_CLIENT_ID, client_secret=SPOTIPY_CLIENT_SECRET)
spotify = spotipy.Spotify(client_credentials_manager=client_credentials_manager)

import requests

TM_URL = "https://app.ticketmaster.com/discovery/v2/"

from model import *

import pprint


def get_venue():
    """ Search in Venues table for venue_name that matches user's request"""

    venue_query = "Slim's"

    payload = {'apikey': CONSUMER_KEY,
                'keyword': venue_query}


    response = requests.get(TM_URL + 'venues',
                            params=payload)

    data = response.json()

    venues = data['_embedded']['venues']

    for i in range(len(venues)):
        print("*****************************\n")
        print(venues[i]['address']['line1'],"\n")
        print(venues[i]['id'],"\n")
        if 'url' in venues[i]:
            print(venues[i]['url'],"\n")
        else:
            print('No url')
            

get_venue()




# def get_events():
#     """ Search in Events table for event_name that matches user's request"""
#     event_query = "Valentine"

#     payload = {'apikey': CONSUMER_KEY,
#                 'keyword': event_query}


#     response = requests.get(TM_URL + 'events',
#                             params=payload)

#     data = response.json()

#     events = data['_embedded']['events']

#     for i in range(len(events)):
#         print("*****************************\n")
#         pprint.pprint(events[i]['name'],"\n"
#                         events[i]['name'],"\n")

# get_events()






def get_artist():
    """ Search in Artists table for artist_name that matches user's request"""
    
    name = 'Radiohead'

    results = spotify.search(q='artist:' + name, type='artist')

    items = results['artists']['items']

    if len(items) > 0:
        artist = items[0]
        print("Spotify_id=", artist['id'],"\n"
            "Artist="+artist['name'],"\n"
            "Artist_URL=","\n"
            "Images=",artist['images'],"\n"
            "Genres=",artist['genres'],"\n"
            "Bio=", artist['external_urls']
            )

#get_artist()





