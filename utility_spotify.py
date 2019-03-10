"""Functions for Spotify API requests, using Spotipy library"""

import os, requests, json

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



def list_top_tracks(artist_spot_ids):
    """Pull an artist's top track URIs from Spotify API"""

    # Determine how many songs to add to playlist
    if len(artist_spot_ids) == 1:
        track_len = 8
    elif len(artist_spot_ids) == 2:
        track_len = 5
    elif len(artist_spot_ids) > 2:
        track_len = 3

    tracks = []

    i = 0

    # List only first five artists of lineup
    while i < 6:
        
        try:
            artist = artist_spot_ids[i]

            try:
                artist_uri = spotify.artist_top_tracks(artist, country='US')

                # List only top tracks
                artist_tracks = []

                j = 0

                while j < track_len:

                    try:
                        track = artist_uri['tracks'][j]['uri']

                    except:
                        break

                    artist_tracks.append(track)
                    j += 1

                # Add all three to all tracks list
                tracks.extend(artist_tracks)

            except:
                continue

        except:
            break

        i += 1

    return tracks


def add_tracks(playlist_id, artist_spot_ids):
    """Post request to Spotify API to add tracks in list to Spotify playlist."""

    tracks = list_top_tracks(artist_spot_ids)

    data = {"uris": tracks}

    headers = {'Authorization': "Bearer " + token,
                'Content-Type': 'application/json'}

    results = requests.post("https://api.spotify.com/v1/playlists/" + playlist_id + "/tracks", data=json.dumps(data), headers=headers)

    return results.json()


def create_playlist(title, artist_spot_ids):
    """Post request to Spotify API to create a new playlist."""

    data = {'name': title,
                'public': True,
                'collaborative': False}

    headers = {'Authorization': "Bearer " + token,
                'Content-Type': 'application/json'}

    results = requests.post("https://api.spotify.com/v1/users/" + USERNAME + "/playlists", data=json.dumps(data), headers=headers)

    json_data = json.loads(results.text)
    
    # Grab playlist id from response.
    playlist_id = json_data['id']

    add_tracks(playlist_id, artist_spot_ids)

    return playlist_id


def update_playlist(playlist_id, artist_spot_ids):
    """Post request to Spotify API to clear then add tracks in list to Spotify playlist."""

    tracks = list_top_tracks(artist_spot_ids)

    data = {'uris': tracks}

    headers = {'Authorization': "Bearer " + token,
                'Content-Type': 'application/json'}

    results = requests.put("https://api.spotify.com/v1/playlists/" + playlist_id + "/tracks", data=json.dumps(data), headers=headers)