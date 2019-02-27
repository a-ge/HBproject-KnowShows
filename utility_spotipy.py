"""Functions for Spotify API requests, using Spotipy library"""
import json
import os

import requests
import pprint
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

sp = spotipy.Spotify(auth=token)


def auth_token():
    print(token)
    data = {'name': "Concert Artists",
                'public': True,
                'collaborative': False}

    headers = {'Authorization': "Bearer " + token,
            'Content-Type': 'application/json'}

    results = requests.post("https://api.spotify.com/v1/users/" + USERNAME + "/playlists", data=json.dumps(data), headers=headers)

    return results


# def create_playlist():


#     playlist_name = "Concert Playlist"
#     desc = "Songs for each artist"
#     playlists = sp.user_playlist_create(USERNAME, playlist_name, desc)
#     # results = spotify.user_playlist_create(USERNAME, playlist_name, desc)

#     pprint.pprint(playlists)

#     scope  = 'playlist-modify-private'
#     token = util.prompt_for_user_token(USERNAME, scope)

#     if token:
#         playlist_name = "Concert Playlist"
#         desc = "Songs for each artist"

#         results = spotify.user_playlist_create("a-ge", playlist_name, desc)
#     else:
#         print("Can't get token for", USERNAME)

# def list_top_track(spotify_uri):
#     """Pull an artist's top track URIs from Spotify API"""

#     # Need to pull artist uri (spotify_id) from db
#     artist_uri = spotify.artist_top_tracks(spotify_uri, country='US')

#     tracks = []

#     for track in artist_uri['tracks']:
#         track_uri = track['uri']
#         tracks.append(track_uri)

#     return artist_top