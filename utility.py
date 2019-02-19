"""Functions API requests"""

import requests
import json

from model import Event, Artist, Lineup, Venue, connect_to_db, db


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

# Will modify later to be able to clean/update db
# For now, trying to seed db with some events in order to test and build other parts of webapp


def find_event_artists(event_id):
    """Call to SeatGeek API for all artists for given event."""

    # Pagination
    pg_payload = {'client_id': CLIENT_ID,
                'client_secret': CLIENT_SECRET,
                'q': event_id}

    pg_response = requests.get(SG_URL + 'performers', params=pg_payload)

    pg_data = pg_response.json()
    # Need to fix!!!!
    total_artists = pg_data['meta']['total'] + 1
    
    results = []
    
    for j in range(1, total_artists):

        payload = {'client_id': CLIENT_ID,
                'client_secret': CLIENT_SECRET,
                'q': event_id,
                'per_page': 20}

        response = requests.get(SG_URL + 'performers', params=payload)

        data = response.json()

        results.append(data)
        
    return set(results)

def find_sg_artists(artist_query):
    """Call to SeatGeek API for all artists given user's artist input."""  

    # Pagination
    pg_payload = {'client_id': CLIENT_ID,
                'client_secret': CLIENT_SECRET,
                'q': artist_query}

    pg_response = requests.get(SG_URL + 'performers', params=pg_payload)

    pg_data = pg_response.json()

    total_artists = pg_data['meta']['total'] + 1

    # Put each page altogether in one list
    results = []

    for j in range(1, total_artists):

        payload = {'client_id': CLIENT_ID,
                'client_secret': CLIENT_SECRET,
                'q': artist_query,
                'per_page': 100}

        response = requests.get(SG_URL + 'performers', params=payload)

        data = response.json()

        results.append(data)


    return results

def list_artist_ids(query):

    if type(query) == 'int':
        results = find_event_artists(query)
    else:
        results = find_sg_artists(query)

    artist_ids = []

    for result in results:
        if result['performers'] != []:
            for i in range(len(result['performers'])):
                artist_id = result['performers'][i]['id']
                artist_ids.append(artist_id)

    return set(artist_ids)


def find_artist_events(artist_id):
    """Call to SeatGeek API for all events for given artist.""" 

    # Pagination
    pg_payload = {'client_id': CLIENT_ID,
                'client_secret': CLIENT_SECRET,
                'venue.country': 'US',
                'performers.id': artist_id}

    pg_response = requests.get(SG_URL + 'events', params=pg_payload)

    pg_data = pg_response.json()

    total_events = pg_data['meta']['total'] + 1

    results = []

    for j in range(1, total_events):

        payload = {'client_id': CLIENT_ID,
                'client_secret': CLIENT_SECRET,
                'venue.country': 'US',
                'performers.id': artist_id,
                'per_page': 10}

        response = requests.get(SG_URL + 'events', params=payload)

        data = response.json()

        results.append(data)
    return results

def find_sg_events(query):
    """Call to SeatGeek API for all events given user's event/venue input."""

    # Pagination
    pg_payload = {'client_id': CLIENT_ID,
                'client_secret': CLIENT_SECRET,
                'venue.country': 'US',
                'q': query,
                'type': "concert"}

    pg_response = requests.get(SG_URL + 'events', params=pg_payload)

    pg_data = pg_response.json()

    total_events = pg_data['meta']['total'] + 1

    # Put each page altogether in one list
    results = []

    for j in range(1, total_events):

        payload = {'client_id': CLIENT_ID,
                'client_secret': CLIENT_SECRET,
                'venue.country': 'US',
                'q': query,
                'type': "concert",
                'per_page': 100}

        response = requests.get(SG_URL + 'events', params=payload)

        data = response.json()

        results.append(data)

    return results

def list_event_ids(query):

    if type(query) == 'int':
        results = find_artist_events(query)
    else:
        results = find_sg_events(query)

    event_ids = []

    for result in results:
        try:
            result['events']
            
            for i in range(len(results['events'])):
                try:
                    event_id = results['events'][i]['id']
                    event_ids.append(event_id)
                except:
                    event_id = None
        except:
            print("oh no*****")

    return set(event_ids)


def find_sg_venues(query):
    """Call to SeatGeek API for all venues given user's event/venue input."""

    # Pagination
    pg_payload = {'client_id': CLIENT_ID,
                'client_secret': CLIENT_SECRET,
                'country': 'US',
                'q': query}

    pg_response = requests.get(SG_URL + 'venues', params=pg_payload)

    pg_data = pg_response.json()

    total_venues = pg_data['meta']['total'] + 1

    # Get all venue_ids that closely match user's input
    results = []

    for j in range(1, total_venues):

        payload = {'client_id': CLIENT_ID,
                'client_secret': CLIENT_SECRET,
                'country': 'US',
                'q': query,
                'per_page': 100}

        response = requests.get(SG_URL + 'venues', params=payload)

        data = response.json()

        results.append(data)

    return results

def list_venue_ids(query):

    results = find_sg_venues(query)

    venue_ids = []

    for result in results:
        try:
            result['venues']
            for i in range(len(result['venues'])):
                venue_id = result['venues'][i]['id']
                venue_ids.append(venue_id)
        except:
            print("oh no*****")

    return set(venue_ids)


def find_venue_events(venue_id):
    """Call to SeatGeek API for all events for given venue."""

    # Pagination
    pg_payload = {'client_id': CLIENT_ID,
                'client_secret': CLIENT_SECRET,
                'venue.id': venue_id}

    pg_response = requests.get(SG_URL + 'events', params=pg_payload)

    pg_data = pg_response.json()

    total_events = pg_data['meta']['total'] + 1

    results = []

    for j in range(1, total_events):

        payload = {'client_id': CLIENT_ID,
                'client_secret': CLIENT_SECRET,
                'venue.id': venue_id,
                'per_page': 100}

        response = requests.get(SG_URL + 'events', params=payload)

        data = response.json()

        results.append(data)

    return results

def list_venue_event_ids(venue_id):  

    results = find_venue_events(venue_id)

    event_ids = []

    for result in results:
        try:
            result['events']
            for i in range(len(result['events'])):
                event_id = result['events'][i]['id']
                event_ids.append(event_id)
        except:
            print("oh no*****")
    return set(event_ids)


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


def insert_lineup(event_id, artist_id):
    # Check if lineup already in db??
    new_lineup = Lineup(event_id=event_id, artist_id=artist_id)
    db.session.add(new_lineup)
    db.session.commit()

def insert_artists(artists):

    for artist in artists:
        
        try:
            Artist.query.filter(Artist.artist_sg_id == artist).one() #????
        # if artist_id not found in db, then insert 
        except: 
            # Call to get artist info
            artist_dict = get_sg_artist(artist)

            # Parse for spotify_id
            try:
                spotify_id_str = artist_dict['performers'][0]['links'][0]['id']
                spot, art, spotify_id = spotify_id_str.split(":") # Can combine two lines??
            except:
                spotify_id = None

            # String genres
            artist_genres = ""
            
            if 'genres' in artist_dict['performers'][0]:
                for i in range(len(artist_dict['performers'][0]['genres'])):
                    genre = artist_dict['performers'][0]['genres'][i]['name']
                    artist_genres = artist_genres + genre + ", "

            try:
                artist_url = artist_dict['performers'][0]['links'][0]['url']
            except:
                artist_url = None

            try:
                artist_photo = artist_dict['performers'][0]['image']
            except:
                artist_photo = None
            # insert into db artist
            new_art = Artist(spotify_id=spotify_id,
                        artist_sg_id=artist,
                        artist_name=artist_dict['performers'][0]['name'],
                        artist_url=artist_url,
                        artist_photo=artist_photo,
                        artist_song="song",
                        artist_genre=artist_genres[:-2])
            print(new_art)
            db.session.add(new_art)
            db.session.commit()
    ## How to instantiate if pulling info from more than one API?
    
def insert_events(events):

    for event in events:
    
        try:
            Event.query.filter(Event.event_sg_id == event).one() #????
        # if event_id not found in db, then insert
        except:
            # Call to get event info
            event_dict = get_sg_event(event)

            try:
                event_url = event_dict['events'][0]['url']
            except:
                event_url = None

            try:
                event_title = event_dict['events'][0]['title']
            except:
                event_title = None

            try:
                event_datetime = event_dict['events'][0]['datetime_utc']
            except:
                event_datetime = None

            try:
                venue_sg_id = event_dict['events'][0]['venue']['id']
                try:
                    venue_obj = Venue.query.filter(Venue.venue_sg_id == venue_sg_id).one()
                    venue_id = venue_obj.venue_id

                except:
                    insert_venues([venue_sg_id])
                    venue_obj = Venue.query.filter(Venue.venue_sg_id == venue_sg_id).one()
                    venue_id = venue_obj.venue_id

            except:
                venue_id = 1

            
            # insert into db event
            new_event = Event(event_sg_id=event,
                            event_title=event_title,
                            event_datetime=event_datetime,
                            event_url=event_url,
                            venue_id=venue_id)
            print(new_event)
            db.session.add(new_event)
            db.session.commit()
            
            if event_dict['events'][0]['performers']:
                for i in range(len(event_dict['events'][0]['performers'])):
                    artists = []
                    artists.append(event_dict['events'][0]['performers'][i]['id'])
                    insert_artists(artists)
                    eve_obj = Event.query.filter(Event.event_sg_id == event).one()
                    art_obj = Artist.query.filter(Artist.artist_sg_id == event_dict['events'][0]['performers'][i]['id']).one()
                    insert_lineup(eve_obj.event_id, art_obj.artist_id)

def insert_venues(venues):

    for venue in venues:
        
        try:
            Venue.query.filter(Venue.venue_sg_id == venue).one() #????
            
        # if venue_id not found in db, then instert
        except:
            # Call to get venue info
            venue_dict = get_sg_venue(venue)

            try:
                venue_name = venue_dict['venues'][0]['name']
            except:
                venue_name = None

            try:
                venue_loc = venue_dict['venues'][0]['location']
            except:
                venue_loc = None

            try:
                venue_url = venue_dict['venues'][0]['url']
            except:
                venue_url = None

            # insert into db venue
            new_venue = Venue(venue_sg_id=venue,
                            venue_name=venue_name,
                            venue_loc=venue_loc,
                            venue_url=venue_url)
            db.session.add(new_venue)
            db.session.commit()
