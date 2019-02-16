"""Seed concerts database from xxxxx"""

# Grab keys from sh file
import os
# SPOTIPY_CLIENT_ID = os.getenv('SPOTIPY_CLIENT_ID')
# SPOTIPY_CLIENT_SECRET = os.getenv('SPOTIPY_CLIENT_SECRET')
# CONSUMER_KEY = os.getenv('CONSUMER_KEY')
SK_KEY = os.getenv('SK_KEY')
CLIENT_SECRET = os.getenv('CLIENT_SECRET')
CLIENT_ID = os.getenv('CLIENT_ID')

# # Spotipy is a Python client library for the Spotify Web API
# import spotipy
# # Spotipy provides a class SpotifyClientCredentials that can be used to authenticate requests
# from spotipy.oauth2 import SpotifyClientCredentials
# client_credentials_manager = SpotifyClientCredentials(client_id=SPOTIPY_CLIENT_ID, client_secret=SPOTIPY_CLIENT_SECRET)
# spotify = spotipy.Spotify(client_credentials_manager=client_credentials_manager)

import requests
import json


#from model import *
#from server import *

SG_URL = "https://api.seatgeek.com/2/"
SK_URL = "https://api.songkick.com/api/3.0/"

def find_sg_events():
    """Call to SeatGeek API for all events."""
    # Will modify later to be able to clean/update db
    # For now, trying to seed db with some events in order to test and build other parts of webapp
    event_query = "Avett"

    payload = {'client_id': CLIENT_ID,
                'client_secret': CLIENT_SECRET,
                'q': event_query,
                'type': "concert"}


    response = requests.get(SG_URL + 'events', params=payload)

    data = response.json()

    events = []

    for i in range(len(data)):
        event_id = data['events'][i]['id']
        events.append(event_id)

    return events


def get_sg_event(event_id):
    """Call to SeatGeek API for a particular event's information. """

    payload = {'client_id': CLIENT_ID,
                'client_secret': CLIENT_SECRET,
                'id': event_id}

    response = requests.get(SG_URL + 'events', params=payload)

    data = response.json()

    return data

    # for j in range(pages):

    #     payload = {'apikey': CONSUMER_KEY,
    #                'city': 'San Francisco',
    #                #'keyword': 'Copeland',
    #                 'startDateTime': '2019-02-14T11:00:00z',
    #                 'endDateTime': '2019-02-15T11:00:00z',
    #                 'page': j}

    #     response = requests.get(TM_URL + 'events',
    #                         params=payload)

    #     data = response.json()

    #     events = data['_embedded']['events']


    #     for i in range(len(events)):
    #         print("*****************************")
    #         print("Event_id=",events[i]['id'])
    #         print("Venue_id=",events[i]['_embedded']['venues'][0]['id'])
    #         event_id = events[i]['id']
    #         get_event_detail(event_id)
            

    #     print(data['page'])

#get_tm_events()

def find_venue():

    venue_query = "a"

    payload = {'apikey': "SK_KEY",
                'query': venue_query}


    response = requests.get(SK_URL + 'search/venues',
                            params=payload)

    data = response.json()

    return data

    # venues = data['resultsPage']['results']

    # for i in range(len(venues)):
    #     print("*****************************")
    #     for key in venues[i]['address']:
    #         print(venues[i]['address'][key],"\n")
    #     for key in venues[i]['city']:
    #         print(venues[i]['city'][key],"\n")
    #     for key in venues[i]['country']:
    #         print(venues[i]['country'][key],"\n")
    #     print(venues[i]['postalCode'],"\n")
    #     print(venues[i]['id'],"\n")
    #     if 'url' in venues[i]:
    #         print(venues[i]['url'],"\n")
    #     else:
    #         print('No url')
    #     print() 

#find_venue()

def get_artist_detail(attraction_id):

    art_payload = {'apikey': CONSUMER_KEY}

    response = requests.get(TM_URL + 'attractions/' + attraction_id, params=art_payload)

    data = response.json()


    print('name=', data['name'])
    print('type=', data['type'])
    print('url=', data['url'])

def get_event_detail(event_id):
    
    ev_payload = {'apikey': CONSUMER_KEY}

    response = requests.get(TM_URL + 'events/' + event_id, params=ev_payload)

    data = response.json()

    print('Event_name=', data['name'])
    print('Event_url=', data['url'])

    attractions = data['_embedded']['attractions']
    for i, attraction in enumerate(attractions):
        attraction_id = attraction['id']
        get_artist_detail(attraction_id)
        

    # attraction_id = data['_embedded']['attractions'][0]['id']
    # get_artist_detail(attraction_id)




# def get_sk_artist():
    
#     name = 'Radiohead'

#     results = spotify.search(q='artist:' + name, type='artist')

#     items = results['artists']['items']

#     if len(items) > 0:
#         artist = items[0]
#         print("Spotify_id=", artist['id'],"\n"
#             "Artist="+artist['name'],"\n"
#             "Artist_URL=","\n"
#             "Images=",artist['images'],"\n"
#             "Genres=",artist['genres'],"\n"
#             "Bio=", artist['external_urls']
#             )

#get_artist()
