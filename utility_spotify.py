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
from spotipy.oauth2 import SpotifyClientCredentials
client_credentials_manager = SpotifyClientCredentials(client_id=SPOTIPY_CLIENT_ID, client_secret=SPOTIPY_CLIENT_SECRET)
spotify = spotipy.Spotify(client_credentials_manager=client_credentials_manager)

scope = 'playlist-modify-public playlist-modify-private'

token = util.prompt_for_user_token(USERNAME, scope)



def list_top_track(artist_spot_id):
    """Pull an artist's top track URIs from Spotify API"""

    # Need to pull artist uri (spotify_id) from db
    artist_uri = spotify.artist_top_tracks(artist_spot_id, country='US')

    tracks = [artist_uri['tracks'][0]['uri'], artist_uri['tracks'][1]['uri'], artist_uri['tracks'][2]['uri']]


    return tracks


def add_tracks(playlist_id, artist_spot_ids):
    
    tracks = []
    for artist in artist_spot_ids:
        artist_tracks = list_top_track('196lKsA13K3keVXMDFK66q')
        tracks.extend(artist_tracks)

    data = {"uris": tracks}

    headers = {'Authorization': "Bearer " + token,
                'Content-Type': 'application/json'}

    results = requests.post("https://api.spotify.com/v1/playlists/" + playlist_id + "/tracks", data=json.dumps(data), headers=headers)

    return results


def create_playlist(artist_spot_ids):

    # https://developer.spotify.com/documentation/web-api/reference/playlists/create-playlist/
    data = {'name': "Concert Artists",
                'public': True,
                'collaborative': False,
                'description': "Top tracks from each artist"}

    headers = {'Authorization': "Bearer " + token,
                'Content-Type': 'application/json'}

    results = requests.post("https://api.spotify.com/v1/users/" + USERNAME + "/playlists", data=json.dumps(data), headers=headers)

    json_data = json.loads(results.text)
    playlist_id = json_data['id']

    add_tracks(playlist_id, artist_spot_ids)

    return playlist_id



