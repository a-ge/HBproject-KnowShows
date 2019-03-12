"""Functions for SeatGeek API requests."""

import os, requests, json

from server import session

CLIENT_SECRET = os.getenv('CLIENT_SECRET')
CLIENT_ID = os.getenv('CLIENT_ID')

SG_URL = "https://api.seatgeek.com/2/"



def get_sg_event(event_id):
    """Call to SeatGeek API for a particular event's information. """

    params = {'client_id': CLIENT_ID,
                'client_secret': CLIENT_SECRET,
                'id': event_id}

    response = requests.get(SG_URL + 'events', params=params)

    return response.json()

def get_sg_venue(venue_id):
    """Call to SeatGeek API for a particular venue's information. """

    params = {'client_id': CLIENT_ID,
                'client_secret': CLIENT_SECRET,
                'id': venue_id}

    response = requests.get(SG_URL + 'venues', params=params)

    return response.json()

def get_sg_artist(artist_id):
    """Call to SeatGeek API for a particular artist's information. """

    params = {'client_id': CLIENT_ID,
                'client_secret': CLIENT_SECRET,
                'id': artist_id}

    response = requests.get(SG_URL + 'performers', params=params)

    return response.json()



def find_sg_artists(artist_query):
    """Call to SeatGeek API for all artists given user's artist input."""  

    params = {'client_id': CLIENT_ID,
                'client_secret': CLIENT_SECRET,
                'q': artist_query,
                'per_page': 20}

    response = requests.get(SG_URL + 'performers', params=params)

    return response.json()



def find_sg_venues(query):
    """Call to SeatGeek API for all venues given user's venue input."""

    city = session['city']

    if session['city'] == '':
        city = None

    state = session['state']

    if session['state'] == '':
        state = None

    params = {'client_id': CLIENT_ID,
                'client_secret': CLIENT_SECRET,
                'city': city,
                'state': state,          
                'country': 'US',
                'q': query,
                'per_page': 20}

    response = requests.get(SG_URL + 'venues', params=params)

    return response.json()


 
def find_artist_events(artist_id, page):
    """Call to SeatGeek API for all events for given artist.""" 

    city = session['city']

    if session['city'] == '':
        city = None

    state = session['state']

    if session['state'] == '':
        state = None
    
    params = {'client_id': CLIENT_ID,
                'client_secret': CLIENT_SECRET,
                'sort': 'datetime_local.asc',
                'performers.id': artist_id,
                'venue.city': city,
                'venue.state': state,
                'venue.country': 'US',
                'per_page': 20,
                'page': page}

    response = requests.get(SG_URL + 'events', params=params)

    return response.json()

def find_sg_events(query, page):
    """Call to SeatGeek API for all events given user's event input."""

    city = session['city']

    if session['city'] == '':
        city = None

    state = session['state']

    if session['state'] == '':
        state = None

    if session['startdate']:
        start_date = session['startdate']
    else:
        start_date = None

    if session['enddate']:
        end_date = session['enddate']
    else:
        end_date = None

    params = {'client_id': CLIENT_ID,
                'client_secret': CLIENT_SECRET,
                'q': query,
                'venue.city': city,
                'venue.state': state,
                'venue.country': 'US',
                'datetime_local.gte': start_date,
                'datetime_local.lte': end_date,
                'type': "concert",
                'sort': 'datetime_local.asc',
                'per_page': 20,
                'page': page}
    
    response = requests.get(SG_URL + 'events', params=params)

    return response.json()

def find_venue_events(venue_id, page):
    """Call to SeatGeek API for all events for given user's venue input."""

    if session['startdate']:
        start_date = session['startdate']
    else:
        start_date = None

    if session['enddate']:
        end_date = session['enddate']
    else:
        end_date = None

    params = {'client_id': CLIENT_ID,
                'client_secret': CLIENT_SECRET,
                'venue.id': venue_id,
                'datetime_local.gte': start_date,
                'datetime_local.lte': end_date,
                'per_page': 20,
                'page': page}

    response = requests.get(SG_URL + 'events', params=params)

    return response.json()
