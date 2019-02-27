"""Functions for SeatGeek API"""

import requests
import json

import os
CLIENT_SECRET = os.getenv('CLIENT_SECRET')
CLIENT_ID = os.getenv('CLIENT_ID')

from server import session

SG_URL = "https://api.seatgeek.com/2/"


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



def find_sg_artists(artist_query):
    """Call to SeatGeek API for all artists given user's artist input."""  

    payload = {'client_id': CLIENT_ID,
            'client_secret': CLIENT_SECRET,
            'q': artist_query,
            'per_page': 10}

    response = requests.get(SG_URL + 'performers', params=payload)

    return response.json()



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

    response = requests.get(SG_URL + 'venues', params=payload)

    return response.json()



def find_artist_events(artist_id):
    """Call to SeatGeek API for all events for given artist.""" 
    print(session['city'], session['state'])
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











