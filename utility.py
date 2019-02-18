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

        # for i in range(len(data['performers'])):
        #     artist_id = data['performers'][i]['id']
        #     artist_ids.append(artist_id)

    return artist_ids

def find_artist_events(artist_id):

    pg_payload = {'client_id': CLIENT_ID,
                'client_secret': CLIENT_SECRET,
                'performers.id': artist_id}

    pg_response = requests.get(SG_URL + 'events', params=pg_payload)

    pg_data = pg_response.json()

    pages = pg_data['meta']['page'] + 1

    event_ids = []

    for j in range(pages):

        payload = {'client_id': CLIENT_ID,
                'client_secret': CLIENT_SECRET,
                'performers.id': artist_id,
                'per_page': 100,
                'page': j}

        response = requests.get(SG_URL + 'events', params=payload)

        data = response.json()

        # for i in range(len(data['events'])):
        #     event_id = data['events'][i]['id']
        #     event_ids.append(event_id)

    return event_ids

def find_sg_events(event_query):
    """Call to SeatGeek API for all events."""
    # Will modify later to be able to clean/update db
    # For now, trying to seed db with some events in order to test and build other parts of webapp

    # Need to get info from all pages!!
    

    pg_payload = {'client_id': CLIENT_ID,
                'client_secret': CLIENT_SECRET,
                'venue.country': 'US',
                'q': event_query,
                'type': "concert"}

    pg_response = requests.get(SG_URL + 'events', params=pg_payload)

    pg_data = pg_response.json()

    pages = pg_data['meta']['page'] + 1

    event_ids = []

    for j in range(pages):

        payload = {'client_id': CLIENT_ID,
                'client_secret': CLIENT_SECRET,
                'venue.country': 'US',
                'q': event_query,
                'type': "concert",
                'per_page': 100,
                'page': j}

        response = requests.get(SG_URL + 'events', params=payload)

        data = response.json()

        # for i in range(len(data['events'])):
        #     event_id = data['events'][i]['id']
        #     event_ids.append(event_id)

    return event_ids

def find_event_artists(event_id):

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

        # for i in range(len(data['performers'])):
        #     artist_id = data['performers'][i]['id']
        #     artist_ids.append(artist_id)

    return artist_ids

def find_sg_venues(venue_query):

    pg_payload = {'client_id': CLIENT_ID,
                'client_secret': CLIENT_SECRET,
                'country': 'US',
                'q': venue_query}

    pg_response = requests.get(SG_URL + 'venues', params=pg_payload)

    pg_data = pg_response.json()

    pages = pg_data['meta']['page'] + 1

    venue_ids = []

    for j in range(pages):

        payload = {'client_id': CLIENT_ID,
                'client_secret': CLIENT_SECRET,
                'q': venue_query,
                'per_page': 100,
                'page': j}

        response = requests.get(SG_URL + 'venues', params=payload)

        data = response.json()

        # for i in range(len(data['venues'])):
        #     venue_id = data['venues'][i]['id']
        #     venue_ids.append(venue_id)

    return venue_ids

def find_venue_events(venue_id):

    pg_payload = {'client_id': CLIENT_ID,
                'client_secret': CLIENT_SECRET,
                'venue.id': event_id}

    pg_response = requests.get(SG_URL + 'events', params=pg_payload)

    pg_data = pg_response.json()

    pages = pg_data['meta']['page'] + 1

    event_ids = []

    for j in range(pages):

        payload = {'client_id': CLIENT_ID,
                'client_secret': CLIENT_SECRET,
                'venue.id': event_id,
                'per_page': 100,
                'page': j}

        response = requests.get(SG_URL + 'events', params=payload)

        data = response.json()

        # for i in range(len(data['events'])):
        #     event_id = data['events'][i]['id']
        #     event_ids.append(event_id)

    return event_ids


def get_sg_event(event_id):
    """Call to SeatGeek API for a particular event's information. """

    payload = {'client_id': CLIENT_ID,
                'client_secret': CLIENT_SECRET,
                'id': event_id}

    response = requests.get(SG_URL + 'events', params=payload)

    return response.json()

def get_sg_venue(venue_id):
    """Call to SeatGeek API for a particular event's information. """

    payload = {'client_id': CLIENT_ID,
                'client_secret': CLIENT_SECRET,
                'id': venue_id}

    response = requests.get(SG_URL + 'venues', params=payload)

    return response.json()

def get_sg_artist(artist_id):
    """Call to SeatGeek API for a particular artist's information. """

    payload = {'client_id': CLIENT_ID,
                'client_secret': CLIENT_SECRET,
                'id': artist_id}

    response = requests.get(SG_URL + 'performers', params=payload)

    return response.json()


def insert_lineups(event_id, artists):

    for artist in artists:
        new_lineup = Lineup(event_id=event_id, artist_id=artist)

def insert_artists(artists):

    for artist in artists:
        
        try:
            Artist.query.filter(Artist.artist_id == artist).one() #????
        # if artist_id not found in db, then instantiate 
        except:    
            # Call to get artist info
            artist_dict = get_sg_artist(artist)

            # Parse for spotify_id
            spotify_id_str = artist_dict['performers'][0]['links'][0]['id']
            spot, art, spotify_id = spotify_id_str.split(":") # Can combine two lines??

            # String genres
            artist_genres = ""
            for i in range(len(artist_dict['performers'][0]['genres'])):
                genre = artist_dict['performers'][0]['genres'][i]['name']
                artist_genres = artist_genres + genre + " "

            # insert into db artist
            new_art = Artist(spotify_id=spotify_id,
                        artist_sg_id=artist_id,
                        artist_name=artist_dict['performers'][0]['name'],
                        artist_url=artist_dict['performers'][0]['links'][0]['url'],
                        artist_photo=artist_dict['performers'][0]['image'],
                        artist_song="song",
                        artist_genre=artist_genres[:-1]) 
    ## How to instantiate if pulling info from more than one API?
    
def insert_events(events):

    for event in events:
    
        try:
            Event.query.filter(Event.event_id == event).one(): #????
        # if event_id not found in db, then instantiate
        except:
            # Call to get event info
            event_dict = get_sg_event(event)
            # insert into db event
            new_event = Event(event_sg_id=event['event_sg_id'],
                            event_title=event['event_title'],
                            event_datetime=event['event_datetime'],
                            event_url=event['event_url'],
                            venue_sg_id=event['venue_sg_id'])
            insert_artists(event_dict['performers'])
            insert_lineups(event, event_dict['performers'])

def insert_venues(venues):

    for venue in venues:
         
        try:
            Venue.query.filter(Venue.venue_id == venue).one(): #????
        # if venue_id not found in db, then instantiate
        except:
            # Call to get venue info
            venue_dict = get_sg_venue(venue)
            # insert into db venue
            new_venue = Venue(venue_sg_id=venue,
                            venue_name=venue_dict['venues'][0]['name'],
                            venue_loc=venue_dict['venues'][0]['location'],
                            venue_url=venue_dict['venues'][0]['url'])