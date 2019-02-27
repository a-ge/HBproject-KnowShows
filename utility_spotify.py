"""Functions for Spotify API requests, using Spotipy library"""
import requests
import json

import os
SPOTIPY_CLIENT_ID = os.getenv('SPOTIPY_CLIENT_ID')
SPOTIPY_CLIENT_SECRET = os.getenv('SPOTIPY_CLIENT_SECRET')
SPOTIPY_REDIRECT_URI= os.getenv('SPOTIPY_REDIRECT_URI')
USERNAME = os.getenv('USERNAME')

# Spotipy is a Python client library for the Spotify Web API
import spotipy
import spotipy.util as util
# Spotipy provides a class SpotifyClientCredentials that can be used to authenticate requests
# from spotipy.oauth2 import SpotifyClientCredentials
# client_credentials_manager = SpotifyClientCredentials(client_id=SPOTIPY_CLIENT_ID, client_secret=SPOTIPY_CLIENT_SECRET)
# spotify = spotipy.Spotify(client_credentials_manager=client_credentials_manager)

scope = 'playlist-modify-public playlist-modify-private'

token = util.prompt_for_user_token(USERNAME, scope)


def create_playlist():

    # https://developer.spotify.com/documentation/web-api/reference/playlists/create-playlist/
    data = {'name': "Concert Artists",
                'public': True,
                'collaborative': False,
                'description': "Top tracks from each artist"}

    headers = {'Authorization': "Bearer " + token,
                'Content-Type': 'application/json'}

    results = requests.post("https://api.spotify.com/v1/users/" + USERNAME + "/playlists", data=json.dumps(data), headers=headers)

    return results



def list_top_track(spotify_uri):
    """Pull an artist's top track URIs from Spotify API"""

    # Need to pull artist uri (spotify_id) from db
    artist_uri = spotify.artist_top_tracks(spotify_uri, country='US')

    tracks = []

    for track in artist_uri['tracks']:
        track_uri = track['uri']
        tracks.append(track_uri)

    return artist_top