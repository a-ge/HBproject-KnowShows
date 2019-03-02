"""Functions for SeatGeek API"""

import requests
import json

import os
YOUR_API_KEY = os.getenv('YOUR_API_KEY')

LASTFM_URL = "http://ws.audioscrobbler.com/2.0/"


def get_artist_bio(artist_name):
    """Call to SeatGeek API for a particular event's information. """

    payload = {'method': 'artist.getinfo',
                'artist': artist_name,
                'api_key': YOUR_API_KEY,
                'format': 'json'}

    response = requests.get(LASTFM_URL, params=payload)

    return response.json()

