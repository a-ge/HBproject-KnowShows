# artist id, name, website, photo, song, genre, bio

# Spotipy is a Python client library for the Spotify Web API
# helps with calls to Spptify API
import spotipy

# Spotipy provides a class SpotifyClientCredentials that can be used to authenticate requests
from spotipy.oauth2 import SpotifyClientCredentials



def get_artist():

    client_credentials_manager = SpotifyClientCredentials()

    spotify = spotipy.Spotify(client_credentials_manager=client_credentials_manager)

    name = 'Radiohead'

    results = spotify.search(q='artist:' + name, type='artist')

    items = results['artists']['items']

    if len(items) > 0:
        artist = items[0]
        print(artist['name'], artist['images'][0]['url'])

get_artist()