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


# Ticketpy is a Python wrapper/SDK for the Ticketmaster Discovery API
import ticketpy
# Calling ApiClient.find() returns a ticketpy.PagedResponse object,
# which iterates through API response pages (as ticketpy.Page)
tm_client = ticketpy.ApiClient(CONSUMER_KEY)

from model import *

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


def get_venue():
    """ Search in Venues table for venue_name that matches user's request"""

    venues = tm_client.venues.find(keyword="Tabernacle").all()

    for v in venues:
        print("Id=", v.id,"\n"
            "Name=", v.name,"\n"
            "Loc=", v.location,"\n"
            "Venue_URL=", v.url
            )

# get_venue()


def get_events():
    """ Search in Events table for event_name that matches user's request"""

    pages = tm_client.events.find(
        keyword="Valentine",
        segment='Music',
        state_code='CA',
        start_date_time='2019-02-14T21:00:00Z',
        end_date_time='2019-02-15T21:00:00Z')

    ## Need to figure out query to venue table
    for page in pages:
        for event in page:
            print("Id=", event.id,"\nName=", event.name,"\n", "Venues=", event.venues)
            #event = Event(event_id=event.id, event_title=event.name)
    #         db.session.add(event)
    # db.session.commit()
    # print(type(pages))
    # print(type(page))
    # print(type(event))
#     <class 'ticketpy.client.PagedResponse'>
#     <class 'ticketpy.model.Page'>
#     <class 'ticketpy.model.Event'>

get_events()