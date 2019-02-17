"""Functions API requests"""

import requests
import json

# Grab keys from sh file
import os
# SPOTIPY_CLIENT_ID = os.getenv('SPOTIPY_CLIENT_ID')
# SPOTIPY_CLIENT_SECRET = os.getenv('SPOTIPY_CLIENT_SECRET')
CLIENT_SECRET = os.getenv('CLIENT_SECRET')
CLIENT_ID = os.getenv('CLIENT_ID')

# # Spotipy is a Python client library for the Spotify Web API
# import spotipy
# # Spotipy provides a class SpotifyClientCredentials that can be used to authenticate requests
# from spotipy.oauth2 import SpotifyClientCredentials
# client_credentials_manager = SpotifyClientCredentials(client_id=SPOTIPY_CLIENT_ID, client_secret=SPOTIPY_CLIENT_SECRET)
# spotify = spotipy.Spotify(client_credentials_manager=client_credentials_manager)

SG_URL = "https://api.seatgeek.com/2/"


def find_sg_events(event_query):
    """Call to SeatGeek API for all events."""
    # Will modify later to be able to clean/update db
    # For now, trying to seed db with some events in order to test and build other parts of webapp

    # Need to get info from all pages!!
    

    pg_payload = {'client_id': CLIENT_ID,
                'client_secret': CLIENT_SECRET,
                'q': event_query,
                'type': "concert"}

    pg_response = requests.get(SG_URL + 'events', params=pg_payload)

    pg_data = pg_response.json()

    pages = pg_data['meta']['page'] + 1

    event_ids = []

    for j in range(pages):

        payload = {'client_id': CLIENT_ID,
            'client_secret': CLIENT_SECRET,
            'q': event_query,
            'type': "concert",
            'per_page': 100,
            'page': j}

        response = requests.get(SG_URL + 'events', params=payload)

        data = response.json()

        for i in range(len(data['events'])):
            event_id = data['events']
            event_ids.append(event_id)

    return set(event_ids)


def get_sg_event(event_id):
    """Call to SeatGeek API for a particular event's information. """

    payload = {'client_id': CLIENT_ID,
                'client_secret': CLIENT_SECRET,
                'id': event_id}

    response = requests.get(SG_URL + 'events', params=payload)

    data = response.json()

    event = {}
    # include short_title of event??
    event['event_title'] = data['events'][0]['title']
    event['event_datetime'] = data['events'][0]['datetime_utc']
    event['event_url'] = data['events'][0]['url']
    event['venue_sg_id'] = data['events'][0]['venue']['id']

    artist_ids = []
    event['artist_ids'] = artist_ids

    for i in range(len(data['events'][0]['performers'])):
        artist_id = data['events'][0]['performers'][i]['id']
        artist_ids.append(artist_id)

    return event


def find_sg_venue(venue_query):

    pg_payload = {'client_id': CLIENT_ID,
                'client_secret': CLIENT_SECRET,
                'q': venue_query}

    pg_response = requests.get(SG_URL + 'venues', params=pg_payload)

    pg_data = pg_response.json()

    pages = pg_data['meta']['page'] + 1

    for j in range(pages):

        payload = {'client_id': CLIENT_ID,
            'client_secret': CLIENT_SECRET,
            'q': venue_query,
            'per_page': 100,
            'page': j}

        response = requests.get(SG_URL + 'venues', params=payload)

        data = response.json()

        venue_ids = []

        for i in range(len(data['venues'])):
            venue_id = data['venues'][i]['id']
            venue_ids.append(venue_id)

    return set(venue_ids)


def get_sg_venue(venue_id):
    """Call to SeatGeek API for a particular event's information. """

    payload = {'client_id': CLIENT_ID,
                'client_secret': CLIENT_SECRET,
                'id': venue_id}

    response = requests.get(SG_URL + 'venues', params=payload)

    data = response.json()

    # event = {}
    # # include short_title of event??
    # event['event_title'] = data['events'][0]['title']
    # event['event_datetime'] = data['events'][0]['datetime_utc']
    # event['event_url'] = data['events'][0]['url']
    # event['venue_sg_id'] = data['events'][0]['venue']['id']

    # artist_ids = []
    # event['artist_ids'] = artist_ids

    # for i in range(len(data['events'][0]['performers'])):
    #     artist_id = data['events'][0]['performers'][i]['id']
    #     artist_ids.append(artist_id)

    return venue


def find_sg_artists(artist_query):
    """Call to SeatGeek API for all events."""  

    pg_payload = {'client_id': CLIENT_ID,
                'client_secret': CLIENT_SECRET,
                'q': artist_query}

    pg_response = requests.get(SG_URL + 'performers', params=pg_payload)

    pg_data = pg_response.json()

    pages = pg_data['meta']['page'] + 1

    artist_ids = []

    for j in range(pages):

        payload = {'client_id': CLIENT_ID,
            'client_secret': CLIENT_SECRET,
            'q': artist_query,
            'per_page': 100,
            'page': j}

        response = requests.get(SG_URL + 'performers', params=payload)

        data = response.json()

        for i in range(len(data['performers'])):
            artist_id = data['performers'][i]['id']
            artist_ids.append(artist_id)

    return set(artist_ids)


def get_sg_artist(artist_id):
    """Call to SeatGeek API for a particular artist's information. """

    payload = {'client_id': CLIENT_ID,
                'client_secret': CLIENT_SECRET,
                'id': artist_id}

    response = requests.get(SG_URL + 'performers', params=payload)

    data = response.json()

    artist = {}

    artist['artist_name'] = data['performers'][0]['name']
    artist['artist_photo'] = data['performers'][0]['image']
    artist['artist_spotify_url'] = data['performers'][0]['links'][0]['url']

    spotify_id_str = data['performers'][0]['links'][0]['id']
    spot, art, spot_id = spotify_id_str.split(":")
    artist['artist_spotify_id'] = spot_id

    artist_genres = []
    artist['artist_genre'] = artist_genres

    for i in range(len(data['performers'][0]['genres'])):
        genre = data['performers'][0]['genres'][i]['name']
        artist_genres.append(genre)

    return artist


def create_lineup(event_id, artist_id):

    pass