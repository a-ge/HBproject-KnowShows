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


def get_artist():

    name = 'Radiohead'

    results = spotify.search(q='artist:' + name, type='artist')

    items = results['artists']['items']

    if len(items) > 0:
        artist = items[0]
        print("Spotify_id=", artist['id'],"\n"
            "Artist="+artist['name'],"\n"
            "Artist_URL=", artist['external_urls'],"\n"
            "Images=",artist['images'],"\n"
            "Genres=",artist['genres'],"\n"
            "Bio=",artist['href']
            )

# get_artist()


def get_venue():

    venues = tm_client.venues.find(keyword="Tabernacle").all()

    for v in venues:
        print("Name: {} / City: {}".format(v.name, v.city))

# get_venue()


def get_events():

    pages = tm_client.events.find(
        classification_name='Hip-Hop',
        state_code='GA',
        start_date_time='2019-02-14T20:00:00Z',
        end_date_time='2019-02-17T20:00:00Z')

    for page in pages:
        for event in page:
            print(event)

get_events()