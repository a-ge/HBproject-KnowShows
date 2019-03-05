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


### Check if playlist for an event already exists??

def list_top_tracks(artist_spot_ids):
    """Pull an artist's top track URIs from Spotify API"""
    print("**test")
    tracks = []

    for artist in artist_spot_ids:
        # Returns list of artist uri's
        try:
            artist_uri = spotify.artist_top_tracks(artist, country='US')
            # List only top three
            artist_tracks = []

            i = 0
            while i < 3:
                try:
                    track = artist_uri['tracks'][i]['uri']
                except:
                    break

                artist_tracks.append(track)
                i += 1

            # Add all three to all tracks list
            tracks.extend(artist_tracks)
        except:
            continue

    return tracks


def add_tracks(playlist_id, artist_spot_ids):
    
    tracks = list_top_tracks(artist_spot_ids)

    data = {"uris": tracks}

    headers = {'Authorization': "Bearer " + token,
                'Content-Type': 'application/json'}

    results = requests.post("https://api.spotify.com/v1/playlists/" + playlist_id + "/tracks", data=json.dumps(data), headers=headers)

    return results.json()


def create_playlist(title, artist_spot_ids):

    # https://developer.spotify.com/documentation/web-api/reference/playlists/create-playlist/
    data = {'name': title,
                'public': True,
                'collaborative': False}

    headers = {'Authorization': "Bearer " + token,
                'Content-Type': 'application/json'}

    results = requests.post("https://api.spotify.com/v1/users/" + USERNAME + "/playlists", data=json.dumps(data), headers=headers)

    json_data = json.loads(results.text)
    playlist_id = json_data['id']

    add_tracks(playlist_id, artist_spot_ids)

    return playlist_id


def update_playlist(playlist_id, artist_spot_ids):

    tracks = list_top_tracks(artist_spot_ids)

    data = {'uris': tracks}

    headers = {'Authorization': "Bearer " + token,
                'Content-Type': 'application/json'}

    # Put will replace, vs post in add_tracks
    results = requests.put("https://api.spotify.com/v1/playlists/" + playlist_id + "/tracks", data=json.dumps(data), headers=headers)