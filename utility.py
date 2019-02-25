"""Functions API requests"""

import requests
import json

import os
CLIENT_SECRET = os.getenv('CLIENT_SECRET')
CLIENT_ID = os.getenv('CLIENT_ID')

SG_URL = "https://api.seatgeek.com/2/"

from model import Event, Artist, Lineup, Venue, connect_to_db, db
from server import session

### To be added later: clean/update db


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
            Artist.query.filter(Artist.artist_sg_id == artist).one()
        except: 
            artist_dict = get_sg_artist(artist)

            try:
                spotify_uri = artist_dict['performers'][0]['links'][0]['id']
            except:
                spotify_uri = None

            try:
                artist_url = artist_dict['performers'][0]['links'][0]['url']
            except:
                artist_url = None

            try:
                artist_photo = artist_dict['performers'][0]['image']
            except:
                artist_photo = None

            # String genres together for now
            artist_genres = ""
            
            if 'genres' in artist_dict['performers'][0]:
                for i in range(len(artist_dict['performers'][0]['genres'])):

                    genre = artist_dict['performers'][0]['genres'][i]['name']
                    artist_genres = artist_genres + genre + ", "

            # insert into db artist
            new_art = Artist(spotify_uri=spotify_uri,
                        artist_sg_id=artist,
                        artist_name=artist_dict['performers'][0]['name'],
                        artist_url=artist_url,
                        artist_photo=artist_photo,
                        artist_genres=artist_genres[:-2])

            db.session.add(new_art)
            db.session.commit()

    ## How to instantiate if pulling info from more than one API?
    ## Possibly not needed since spotify id provided in SeatGeek

def insert_venues(venues):

    for venue in venues:
        
        try:
            Venue.query.filter(Venue.venue_sg_id == venue).one()
        except:
            venue_dict = get_sg_venue(venue)

            try:
                venue_name = venue_dict['venues'][0]['name']
            except:
                venue_name = None

            try:
                venue_add = venue_dict['venues'][0]['address']
            except:
                venue_add = None

            try:
                venue_extend_add = venue_dict['venues'][0]['extended_address']
            except:
                venue_extend_add = None

            try:
                venue_lat = venue_dict['venues'][0]['location']['lat']
            except:
                venue_lat = None

            try:
                venue_lng = venue_dict['venues'][0]['location']['lon']
            except:
                venue_lng = None

            try:
                venue_url = venue_dict['venues'][0]['url']
            except:
                venue_url = None

            try:
                venue_upcoming = venue_dict['venues'][0]['has_upcoming_events']
            except:
                venue_upcoming = None

            # insert into db
            new_venue = Venue(venue_sg_id=venue,
                            venue_name=venue_name,
                            venue_add=venue_add,
                            venue_extend_add=venue_extend_add,
                            venue_lat=venue_lat,
                            venue_lng=venue_lng,
                            venue_url=venue_url,
                            venue_upcoming=venue_upcoming)

            db.session.add(new_venue)
            db.session.commit()

def insert_events(events):

    for event in events:
    
        try:
            print("*************", event_dict['events'][0]['venue'])
            venue_sg_id = event_dict['events'][0]['venue']['id']

            try:
                venue_obj = Venue.query.filter(Venue.venue_sg_id == venue_sg_id).one()
            except:
                insert_venues([venue_sg_id])
                venue_obj = Venue.query.filter(Venue.venue_sg_id == venue_sg_id).one()
            venue_id = venue_obj.venue_id

        except:
            venue_id = None

        try:
            Event.query.filter(Event.event_sg_id == event).one()
        except:
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
                event_datetime = event_dict['events'][0]['datetime_local']
            except:
                event_datetime = None



            
            # insert into db
            new_event = Event(venue_id=venue_id,
                            event_sg_id=event,
                            event_title=event_title,
                            event_datetime=event_datetime,
                            event_url=event_url)

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



def list_event_artists(event_id):


    event_lineups = Lineup.query.filter(Lineup.event_id == event_id).all()
             
    event_artists = [Artist.query.filter(Artist.artist_id == lineup.artist_id).one() for lineup in event_lineups]
    
    art = {}

    for i, art_obj in enumerate(event_artists):

        art_obj = Artist.query.filter(Artist.artist_id == art_obj.artist_id).one()
        art['artist' + str(i + 1)] = art_obj

    return art



def find_sg_artists(artist_query):
    """Call to SeatGeek API for all artists given user's artist input."""  

    payload = {'client_id': CLIENT_ID,
            'client_secret': CLIENT_SECRET,
            'q': artist_query,
            'per_page': 10}

    response = requests.get(SG_URL + 'performers', params=payload)

    return response.json()

def list_artist_ids(query):

    results = find_sg_artists(query)

    artist_ids = []

    if results['performers'] != []:
        for i in range(len(results['performers'])):

            if results['performers'][i]['has_upcoming_events'] == True:

                artist_id = results['performers'][i]['id']
                artist_ids.append(artist_id)

        insert_artists(artist_ids)

        return set(artist_ids)

    else:
        return ""



def find_artist_events(artist_id):
    """Call to SeatGeek API for all events for given artist.""" 

    payload = {'client_id': CLIENT_ID,
            'client_secret': CLIENT_SECRET,
            'performers.id': artist_id,
            'venue.city': session['city'],
            'venue.state': session['state'],
            'venue.country': 'US',
            'lat': session['lat'],
            'lon': session['lon'],
            'per_page': 10}

    response = requests.get(SG_URL + 'events', params=payload)

    return response.json()

def find_sg_events(query):
    """Call to SeatGeek API for all events given user's event input."""

    payload = {'client_id': CLIENT_ID,
            'client_secret': CLIENT_SECRET,
            'q': query,
            'venue.city': session['city'],
            'venue.state': session['state'],
            'venue.country': 'US',
            'lat': session['lat'],
            'lon': session['lon'],
            'type': "concert",
            'per_page': 10}
    
    response = requests.get(SG_URL + 'events', params=payload)

    return response.json()

def list_event_ids(query):

    if type(query) == int:
        results = find_artist_events(query)

    else:
        results = find_sg_events(query)

    event_ids = []

    if results['events']:
        for i in range(len(results['events'])):

            if results['events'][i]['id']:

                event_id = results['events'][i]['id']
                event_ids.append(event_id)

        insert_events(event_ids)

        return set(event_ids)

    else:
        return ""
        


def find_sg_venues(query):
    """Call to SeatGeek API for all venues given user's venue input."""

    payload = {'client_id': CLIENT_ID,
            'client_secret': CLIENT_SECRET,
            'city': session['city'],
            'state': session['state'],          
            'country': 'US',
            'lat': session['lat'],
            'lon': session['lon'],
            'q': query,
            'per_page': 10}
    print(payload)
    response = requests.get(SG_URL + 'venues', params=payload)

    return response.json()

def list_venue_ids(query):

    results = find_sg_venues(query)

    venue_ids = []

    if results['venues']:
        for i in range(len(results['venues'])):

            if results['venues'][i]['has_upcoming_events'] == True:

                venue_id = results['venues'][i]['id']
                venue_ids.append(venue_id)

        insert_venues(venue_ids)

        return set(venue_ids)

    else:
        return ""


# Need to determine how start_date and end_date will be set as arguments
def find_venue_events(venue_id, start_date=None, end_date=None):
    """Call to SeatGeek API for all events for given venue."""

    payload = {'client_id': CLIENT_ID,
            'client_secret': CLIENT_SECRET,
            'venue.id': venue_id,
            'datetime_utc.gte': start_date,
            'datetime_utc.lte': end_date,
            'per_page': 10}

    response = requests.get(SG_URL + 'events', params=payload)

    return response.json()

def list_venue_event_ids(venue_id):  


    results = find_venue_events(venue_id)

    event_ids = []

    if results['events']:
        for i in range(len(results['events'])):

            event_id = results['events'][i]['id']
            event_ids.append(event_id)

        insert_events(event_ids)

        return set(event_ids)

    else:
        return ""



