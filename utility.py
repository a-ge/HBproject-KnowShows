# artist id, name, website, photo, genre, bio, **song
# event id, event title, event date, event time, event url
# venue name, venue location, venue url?


# Spotipy is a Python client library for the Spotify Web API
import spotipy
# Spotipy provides a class SpotifyClientCredentials that can be used to authenticate requests
from spotipy.oauth2 import SpotifyClientCredentials

client_credentials_manager = SpotifyClientCredentials()

spotify = spotipy.Spotify(client_credentials_manager=client_credentials_manager)


# Ticketpy is a Python wrapper/SDK for the Ticketmaster Discovery API
import ticketpy

tm_client = ticketpy.ApiClient('ticket_api_key')


def get_artist():

    name = 'Radiohead'

    results = spotify.search(q='artist:' + name, type='artist')

    items = results['artists']['items']

    if len(items) > 0:
        artist = items[0]
        print("Spotify_id="+artist['id'],"\n"
            "Artist="+artist['name'],"\n"
            "Artist_URL=", artist['external_urls'],"\n"
            "Images=",artist['images'],"\n"
            "Genres=",artist['genres'],"\n"
            "Bio=",artist['href']
            )

get_artist()


# def get_venue():

#     venues = tm_client.venues.find(keyword="Tabernacle").all()

#     for v in venues:
#         print("Name: {} / City: {}".format(v.name, v.city))

# get_venue()


# def get_events():

#     pages = tm_client.events.find(
#         classification_name='Hip-Hop',
#         state_code='GA',
#         start_date_time='2017-05-19T20:00:00Z',
#         end_date_time='2017-05-21T20:00:00Z')

#     for page in pages:
#         for event in page:
#             print(event)

# get_events()