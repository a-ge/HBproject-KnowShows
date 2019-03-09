"""Functions for Concerts Database and functions call to Last.FM and GoogleMaps APIs."""

import os, requests, json, googlemaps
from datetime import datetime

from model import Event, Artist, Lineup, Venue, connect_to_db, db
from server import session
from utility_seatgeek import *
from utility_spotify import *



def get_artist_bio(artist_name):
    """Call to Last.FM API for a particular artist's bio. """

    LFM_API_KEY = os.getenv('LFM_API_KEY')

    LFM_URL = "http://ws.audioscrobbler.com/2.0/"

    payload = {'method': 'artist.getinfo',
                'artist': artist_name,
                'api_key': LFM_API_KEY,
                'format': 'json'}

    response = requests.get(LFM_URL, params=payload)

    return response.json()



def convert_latlng(lat, lng):
    """Call to Google Maps Geocoding API to convert lat/lng to city and state of user. """

    API_KEY = os.getenv('API_KEY')

    gmaps = googlemaps.Client(API_KEY)

    response = gmaps.reverse_geocode(latlng=(lat, lng))

    return response



def modify_artist_playlist_id(artist, artist_spot_id):
    """Check db if a Spotify playlist already exists for the artist, then create or update a playlist."""

    if artist.artist_sp_playlist_id:

        playlist_id = artist.artist_sp_playlist_id

        update_playlist(playlist_id, artist_spot_id)

    else:
        title = "KnowShows- " + artist.artist_name 

        playlist_id = create_playlist(title, artist_spot_id)

        # Initial playlist created, so add/replace None playlist_id in db
        Artist.query.filter(Artist.artist_id == artist.artist_id).update({'artist_sp_playlist_id': playlist_id})

        db.session.commit()

    return playlist_id

def modify_event_playlist_id(event, artist_spot_ids):
    """Check db if a Spotify playlist already exists for the event, then create or update a playlist."""

    if event.event_sp_playlist_id:

        playlist_id = event.event_sp_playlist_id

        update_playlist(playlist_id, artist_spot_ids)

    else:
        title = event.event_title + "\n" + event.venue.venue_name + "\n" + str(event.event_datetime)

        playlist_id = create_playlist(title, artist_spot_ids)

        # Initial playlist created, so add/replace None playlist_id in db
        Event.query.filter(Event.event_id == event.event_id).update({'event_sp_playlist_id': playlist_id})

        db.session.commit()

    return playlist_id



def insert_lineup(event_id, artist_id):
    """Instantiate into db Lineup table a lineup record with given event_id and artist_id."""

    new_lineup = Lineup(event_id=event_id, artist_id=artist_id)
    db.session.add(new_lineup)
    db.session.commit()

def insert_artists(artists):
    """Instantiate into db Artists table an artist record."""

    for artist in artists:
        
        try:
            # Check if artist's SeatGeek id is already in db.
            Artist.query.filter(Artist.artist_sg_id == artist).one()
        except: 
            # If not in db, create artist record with SeatGeek response.
            artist_dict = get_sg_artist(artist)

            try:
                spotify_uri = artist_dict['performers'][0]['links'][0]['id']
            except:
                spotify_uri = None

            try:
                artist_name = artist_dict['performers'][0]['name']
            except:
                artist_name = "Artist Name"

            try:
                artist_url = artist_dict['performers'][0]['links'][0]['url']
            except:
                artist_url = None

            try:
                artist_photo = artist_dict['performers'][0]['image']
            except:
                artist_photo = "https://seatgeek.com/images/performers-landscape/trippin-billies-e69c14/1947/huge.jpg"

            try:
                artist_dict['performers'][0]['genres']

                artist_genres = ""
                for i in range(len(artist_dict['performers'][0]['genres'])):

                    genre = artist_dict['performers'][0]['genres'][i]['name']
                    artist_genres = artist_genres + genre + ", "
            except:
                artist_genres = "  "

            # Insert into db.
            new_art = Artist(spotify_uri=spotify_uri,
                        artist_sg_id=artist,
                        artist_name=artist_name,
                        artist_url=artist_url,
                        artist_photo=artist_photo,
                        artist_genres=artist_genres[:-2],
                        artist_bio=None)

            db.session.add(new_art)
            db.session.commit()

            # Add artist's bio with Last.FM response.
            art = Artist.query.filter(Artist.artist_sg_id == artist).one()
            art_sum = get_artist_bio(art.artist_name)

            try:
                art_sum['artist']['bio']['summary']
                art_bio, art_url = art_sum['artist']['bio']['summary'].split("<a href=")
            except:
                art_bio = "Artist bio not found. Just give 'em a listen and enjoy."
                
            Artist.query.filter(Artist.artist_id == art.artist_id).update({'artist_bio': str(art_bio)})
            db.session.commit()

def insert_venues(venues):
    """Instantiate into db Venues table a venue record."""

    for venue in venues:
        
        try:
            # Check if venue's SeatGeek id is already in db.
            Venue.query.filter(Venue.venue_sg_id == venue).one()
        except:
            # If not in db, create venue record with SeatGeek response.
            venue_dict = get_sg_venue(venue)

            if venue_dict['venues'][0]['name'] == None:
                venue_name = "Venue name"
            else:
                venue_name = venue_dict['venues'][0]['name']

            if venue_dict['venues'][0]['address'] == None:
                venue_add = "Address"
            else:
                venue_add = venue_dict['venues'][0]['address']

            if venue_dict['venues'][0]['city'] == None:
                venue_city = "Venue City"
            else:
                venue_city = venue_dict['venues'][0]['city']

            if venue_dict['venues'][0]['state'] == None:
                venue_state = "ST"
            else:
                venue_state = venue_dict['venues'][0]['state']

            if venue_dict['venues'][0]['postal_code'] == None:
                venue_zip = "12492"
            else:
                venue_zip = venue_dict['venues'][0]['postal_code']

            # Insert into db.
            new_venue = Venue(venue_sg_id=venue,
                            venue_name=venue_name,
                            venue_add=venue_add,
                            venue_city=venue_city,
                            venue_state=venue_state,
                            venue_zip=venue_zip)

            db.session.add(new_venue)
            db.session.commit()

def insert_events(events):
    """Instantiate into db Events table an event record."""
    for event in events:

        try:
            # Check if event's SeatGeek id is already in db.
            Event.query.filter(Event.event_sg_id == event).one()
        except:
            # If not in db, create event record with SeatGeek response.
            event_dict = get_sg_event(event)

            try:
                venue_sg_id = event_dict['events'][0]['venue']['id']
                insert_venues([venue_sg_id])
                venue_obj = Venue.query.filter(Venue.venue_sg_id == venue_sg_id).one()
                venue_id = venue_obj.venue_id

            except:
                venue_id = None

            try:
                event_url = event_dict['events'][0]['url']
            except:
                event_url = "https://seatgeek.com/"

            try:
                event_title = event_dict['events'][0]['title']
            except:
                event_title = "Concert Title"

            try:
                d = datetime.strptime(event_dict['events'][0]['datetime_local'], '%Y-%m-%dT%H:%M:%S')
                event_datetime = d.strftime('%b %d, %Y   %H:%M')
            except:
                event_datetime = None

            
            # Insert into db.
            new_event = Event(venue_id=venue_id,
                            event_sg_id=event,
                            event_title=event_title,
                            event_datetime=event_datetime,
                            event_url=event_url,
                            event_sp_playlist_id=None)

            db.session.add(new_event)
            db.session.commit()

            # Add each artist in event to the db and then create their lineup record.
            if event_dict['events'][0]['performers']:

                artists = []

                for i in range(len(event_dict['events'][0]['performers'])):

                    artists.append(event_dict['events'][0]['performers'][i]['id'])
                
                insert_artists(artists)

                eve_obj = Event.query.filter(Event.event_sg_id == event).one()

                for artist in artists:
                    art_obj = Artist.query.filter(Artist.artist_sg_id == artist).one()
                    insert_lineup(eve_obj.event_id, art_obj.artist_id)



def list_event_artists(event_id):
    """Create a dictionary with all artist_ids for a particular event."""

    # Query db for all lineup records for event.
    event_lineups = Lineup.query.filter(Lineup.event_id == event_id).all()
    
    # Query db for each artist object.     
    event_artists = [Artist.query.filter(Artist.artist_id == lineup.artist_id).one() for lineup in event_lineups]
    
    art = {}

    for i, art_obj in enumerate(event_artists):

        art_obj = Artist.query.filter(Artist.artist_id == art_obj.artist_id).one()

        art['artist' + str(i + 1)] = art_obj

    return art

def list_artist_ids(query, page):
    """Create tuple with total number of artists found in SeatGeek
    and a list of the artist_ids found on page number argument."""

    # Response from SeatGeek call.
    results = find_sg_artists(query, page)

    total_artists = results['meta']['total']

    artist_ids = []

    if results['performers'] != []:
        for i in range(len(results['performers'])):

            if results['performers'][i]['has_upcoming_events'] == True:

                artist_id = results['performers'][i]['id']

                if artist_id not in artist_ids:
                    artist_ids.append(artist_id)

        insert_artists(artist_ids)

        return (total_artists, artist_ids)

def list_event_ids(query, page):
    """Create tuple with total number of events found in SeatGeek
    and a list of the event_ids found on page number argument."""

    # Query passed in will either be an integer for a particular artist's SG id
    # or a string for user's input in search textbox.
    if type(query) == int:
        results = find_artist_events(query, page)

    else:
        results = find_sg_events(query, page)

    total_events = results['meta']['total']

    event_ids = []

    if results['events']:
        for i in range(len(results['events'])):

            if results['events'][i]['id']:

                event_id = results['events'][i]['id']

                if event_id not in event_ids:
                    event_ids.append(event_id)

        insert_events(event_ids)

    return (total_events, event_ids)

def list_venue_ids(query, page):
    """Create tuple with total number of venues found in SeatGeek
    and a list of the venue_ids found on page number argument."""

    # Response from SeatGeek call.
    results = find_sg_venues(query, page)

    total_venues = results['meta']['total']

    venue_ids = []

    if results['venues']:
        for i in range(len(results['venues'])):

            if results['venues'][i]['has_upcoming_events'] == True:
                
                venue_id = results['venues'][i]['id']

                if venue_id not in venue_ids:
                    venue_ids.append(venue_id)

        insert_venues(venue_ids)

    return (total_venues, venue_ids)

def list_venue_event_ids(venue_id, page):  
    """Create tuple with total number of events found in SeatGeek for a particular venue
    and a list of the event_ids found on page number argument."""

    # User has option to enter a start/end date range.
    # If session has date(s), include in call to SeatGeek API.
    if session['startdate']:
        start_date = session['startdate']
    else:
        start_date  = None

    if session['enddate']:
        end_date = session['enddate']
    else:
        end_date  = None

    # Response from SeatGeek call.
    results = find_venue_events(venue_id, page)

    total_events = results['meta']['total']

    event_ids = []

    if results['events']:
        for i in range(len(results['events'])):

            event_id = results['events'][i]['id']

            if event_id not in event_ids:
                event_ids.append(event_id)

        insert_events(event_ids)

    return (total_events, event_ids)
