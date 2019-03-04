"""Functions for SeatGeek API"""

import requests
import json
import pprint

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
    """Call to SeatGeek API for a particular venue's information. """

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

    # if session['lat']:
    #     payload = {'client_id': CLIENT_ID,
    #             'client_secret': CLIENT_SECRET,        
    #             'country': 'US',
    #             'lat': session['lat'],
    #             'lon': session['lon'],
    #             'q': query,
    #             'per_page': 10}

    # else:
    payload = {'client_id': CLIENT_ID,
            'client_secret': CLIENT_SECRET,
            'city': session['city'],
            'state': session['state'],          
            'country': 'US',
            'q': query,
            'per_page': 10}

    response = requests.get(SG_URL + 'venues', params=payload)

    return response.json()



def find_artist_events(artist_id):
    """Call to SeatGeek API for all events for given artist.""" 


    # if session['lat']:
    #     payload = {'client_id': CLIENT_ID,
    #             'client_secret': CLIENT_SECRET,
    #             'performers.id': artist_id,
    #             'venue.country': 'US',
    #             'lat': session['lat'],
    #             'lon': session['lon'],
    #             'per_page': 10}

    # else:
    payload = {'client_id': CLIENT_ID,
        'client_secret': CLIENT_SECRET,
        'sort': 'datetime_local.asc',
        'performers.id': artist_id,
        'venue.city': session['city'],
        'venue.state': session['state'],
        'venue.country': 'US',
        'per_page': 10}

    response = requests.get(SG_URL + 'events', params=payload)

    return response.json()

def find_sg_events(query):
    """Call to SeatGeek API for all events given user's event input."""

    # if session['lat']:
    #     payload = {'client_id': CLIENT_ID,
    #             'client_secret': CLIENT_SECRET,
    #             'q': query,
    #             'venue.country': 'US',
    #             'lat': session['lat'],
    #             'lon': session['lon'],
    #             'type': "concert",
    #             'per_page': 10}
    # else:

    if session['startdate']:
        start_date = session['startdate']
    else:
        start_date  = None

    if session['enddate']:
        end_date = session['enddate']
    else:
        end_date  = None

    payload = {'client_id': CLIENT_ID,
            'client_secret': CLIENT_SECRET,
            'q': query,
            'venue.city': session['city'],
            'venue.state': session['state'],
            'venue.country': 'US',
            'datetime_local.gte': start_date,
            'datetime_local.lte': end_date,
            'type': "concert",
            'per_page': 10}
    
    response = requests.get(SG_URL + 'events', params=payload)

    return response.json()
# Need to determine how start_date and end_date will be set as arguments
def find_venue_events(venue_id):
    """Call to SeatGeek API for all events for given user's venue input."""

    if session['startdate']:
        start_date = session['startdate']
    else:
        start_date  = None

    if session['enddate']:
        end_date = session['enddate']
    else:
        end_date  = None

    payload = {'client_id': CLIENT_ID,
            'client_secret': CLIENT_SECRET,
            'venue.id': venue_id,
            'datetime_local.gte': start_date,
            'datetime_local.lte': end_date,
            'per_page': 10}

    response = requests.get(SG_URL + 'events', params=payload)

    return response.json()
