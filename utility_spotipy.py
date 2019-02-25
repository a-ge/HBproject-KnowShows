"""Functions for Spotify API requests, using Spotipy library"""

import os
SPOTIPY_CLIENT_ID = os.getenv('SPOTIPY_CLIENT_ID')
SPOTIPY_CLIENT_SECRET = os.getenv('SPOTIPY_CLIENT_SECRET')

# Spotipy is a Python client library for the Spotify Web API
import spotipy
# Spotipy provides a class SpotifyClientCredentials that can be used to authenticate requests
from spotipy.oauth2 import SpotifyClientCredentials
client_credentials_manager = SpotifyClientCredentials(client_id=SPOTIPY_CLIENT_ID, client_secret=SPOTIPY_CLIENT_SECRET)
spotify = spotipy.Spotify(client_credentials_manager=client_credentials_manager)



def create_playlist():

    user_id = "fyh4z44svl2nstrnz0ii6hts3"
    playlist_name = "Concert Playlist"
    desc = "Songs for each artist"

    results = spotify.user_playlist_create(user_id, playlist_name, desc)


def list_top_track(spotify_uri):
    """Pull an artist's top track URIs from Spotify API"""

    # Need to pull artist uri (spotify_id) from db
    artist_uri = spotify.artist_top_tracks(spotify_uri, country='US')

    tracks = []

    for track in artist_uri['tracks']:
        track_uri = track['uri']
        tracks.append(track_uri)

    return artist_top