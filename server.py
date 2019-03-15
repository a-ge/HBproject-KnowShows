"""View functions for KnowShows webapp."""

import os, math
from jinja2 import StrictUndefined
from flask import Flask, render_template, redirect, request, flash, session, jsonify
from flask_debugtoolbar import DebugToolbarExtension
from datetime import datetime

from model import Event, Artist, Lineup, Venue, connect_to_db, db
from utility import *

app = Flask(__name__)

# Required to use Flask sessions and the debug toolbar
app.secret_key = os.getenv("secret_key")

# Normally, if you use an undefined variable in Jinja2, it fails silently.
# This is horrible. Fix this so that, instead, it raises an error.
app.jinja_env.undefined = StrictUndefined



@app.route('/')
def index():
    """Homepage."""

    return render_template("homepage.html")


@app.route('/loc', methods=["GET", "POST"])
def get_location():
    """Get lat/lng from GoogleMaps to convert to City/State, then send to populate search form."""

    if request.method == "POST":

        # When user clicks "Find my location" button, this pulls info from Google Maps Geolocation API response.
        lat = request.json['lat']
        lng = request.json['lng']

        # Call to Google Maps Reverse Geocoding API.
        results = convert_latlng(lat, lng)

        # Find city and state from results and add to session.
        for i in range(len(results[0]['address_components'])):

            if results[0]['address_components'][i]['types'][0] == 'locality':

                session['city'] = results[0]['address_components'][i]['long_name']

            if results[0]['address_components'][i]['types'][0] == 'administrative_area_level_1':

                session['state'] = results[0]['address_components'][i]['short_name']

                break

    # City and state sent to base.html to populate city and state text boxes.          
    data ={'city': session['city'],
            'state': session['state']}

    return jsonify(data)


@app.route('/search', methods=['POST'])
def search():
    """ Retrieve user's search inputs, add them to session, and then redirect to correct page."""

    if request.method == "POST":

        # When user clicks "Search" button add information to session.
        query_type = request.form['searchType']

        session['user_query'] = request.form['userSearchInput']

        city = request.form['userCityInput']
        if city == "":
            session['city'] = None
        else:
            session['city'] = city

        state = request.form['state']
        if state == "":
            session['state'] = None
        else:
            session['state'] = state

        start_date = request.form['startdate']
        if start_date == "":
            session['startdate'] = None
        else:
            d = datetime.strptime(start_date, '%m/%d/%Y')
            session['startdate'] = d.strftime('%Y-%m-%d')
        
        end_date = request.form['enddate']
        if end_date == "":
            session['enddate'] = None
        else:
            d = datetime.strptime(end_date, '%m/%d/%Y')
            session['enddate'] = d.strftime('%Y-%m-%d')

    if query_type == "Artist":
        return redirect("/check_artist")

    elif query_type == "Venue":
        return redirect("/check_venue")

    elif query_type == "Event":
        return redirect("/check_event/1")


@app.route('/check_artist')
def check_artist():
    """List artists found that closely match artist entered by user."""

    # Search db, then if necessary, call API for artists,
    # response is a list of artist_sg_ids.
    artist_sg_info  = list_artist_ids(session['user_query'])

    # Get each artist object for each artist_sg_id.
    artist_options = [Artist.query.filter(Artist.artist_sg_id == artist).one() for artist in artist_sg_info]

    # If only one artist found, go directly to the artist's page.
    if len(artist_options) == 1:
        artist_id = artist_options[0].artist_id
        return redirect("/artist/" + str(artist_id) + "/1")

    else:
        return render_template("check_artist.html", artist_options=artist_options)


@app.route('/artist/<artist_id>/<int:page>')
def display_artist(artist_id, page):
    """List all events with their lineup artists for artist selected."""

    # Find artist object of artist_id.
    artist_select = Artist.query.filter(Artist.artist_id == artist_id).one()

    # Search db, then if necessary, call API for all events of a particular artist,
    # response is a tuple with total items and a list of event_sg_ids.
    artist_sg_info = list_event_ids(artist_select.artist_sg_id, page)

    # Knowing total items, calculate total pages.
    total_pages = math.ceil(artist_sg_info[0] / 50)

    # Create a list with nested lists where event obj in index 0
    # and following indexes are the artist objs for given event.
    artist_event_dicts = []
    
    for event in artist_sg_info[1]:

        eve = []

        eve_obj = Event.query.filter(Event.event_sg_id == event).one()

        # First add event object.
        eve.append(eve_obj)

        # Get dictionary with each artist object.
        eve.append(list_event_artists(eve_obj.event_id))

        artist_event_dicts.append(eve)

    playlist_id = modify_artist_playlist_id(artist_select)

    return render_template("artist.html", artist=artist_select,
                                            artist_event_dicts=artist_event_dicts,
                                            playlist_id=playlist_id,
                                            total_pages=total_pages,
                                            current_page=page)


@app.route('/check_venue')
def check_venue():
    """List venues found that closely match venue entered by user."""

    # Search db, then if necessary, call API for venues,
    # response is a list of venue_sg_ids.
    venue_sg_info = list_venue_ids(session['user_query'])

    # Get each venue object for each venue_sg_id.
    venue_options = [Venue.query.filter(Venue.venue_sg_id == venue).one() for venue in venue_sg_info]

    # If only one venue found, go directly to the venue's page.
    if len(venue_options) == 1:
        venue_id = venue_options[0].venue_id
        return redirect("/venue/" + str(venue_id) + "/1")

    return render_template("check_venue.html", venue_options=venue_options)


@app.route('/venue/<venue_id>/<int:page>')
def display_venue(venue_id, page):
    """List all events with lineups artists for venue selected."""
    
    # Find venue object
    venue_select = Venue.query.filter(Venue.venue_id == venue_id).one()

    # Search db, then if necessary, call API for all events of a particular venue,
    # response is a tuple with total items and a list of event_sg_ids.
    venue_sg_info = list_venue_event_ids(venue_select.venue_sg_id, page)

    # Knowing total items, calculate total pages.
    total_pages = math.ceil(venue_sg_info[0] / 20)

    # Create a list with nested lists where venue obj in index 0
    # and following indexes are the event objs for given venue.
    venue_event_dicts = []
    
    for event in venue_sg_info[1]:

        eve = []

        eve_obj = Event.query.filter(Event.event_sg_id == event).one()

        # First add event object.
        eve.append(eve_obj)

        # Get a list with each artist object.
        eve.append(list_event_artists(eve_obj.event_id))

        venue_event_dicts.append(eve)

    return render_template("venue.html", venue=venue_select,
                                            venue_event_dicts=venue_event_dicts,
                                            total_pages=total_pages,
                                            current_page=page)


@app.route('/check_event/<int:page>')
def check_event(page):
    """List events found that closely match event entered by user."""

    # Search db, then if necessary, call API for events,
    # response is a tuple with total items and a list of event_sg_ids.
    event_sg_info = list_event_ids(session['user_query'], page)

    # Knowing total items, calculate total pages.
    total_pages = math.ceil(event_sg_info[0]/20)

    # Get each event object for each event_sg_id.
    event_options = [Event.query.filter(Event.event_sg_id == event).one() for event in event_sg_info[1]]

    # If only one event found, go directly to the event's page.
    if len(event_options) == 1:
        event_id = event_options[0].event_id
        return redirect("/event/" + str(event_id))

    return render_template("check_event.html", event_options=event_options,
                                                total_pages=total_pages,
                                                current_page=page)


@app.route('/event/<event_id>')
def display_event(event_id):
    """Display event information."""
    
    # Find event object of event_id.
    event_select = Event.query.filter(Event.event_id == event_id).one()

    # Create a dictionary with each artist in the event.
    event_dicts = list_event_artists(event_id)

    # List all the Spotify id's for each artist.
    artist_spot_ids = [value.spotify_uri for key, value in event_dicts.items()]

    # Create Spotify playlist for the event.
    playlist_id = modify_event_playlist_id(event_select, artist_spot_ids)
 
    return render_template("event.html", event=event_select,
                                            event_dicts=event_dicts,
                                            playlist_id=playlist_id)




if __name__ == "__main__":
    # We have to set debug=True here, since it has to be True at the
    # point that we invoke the DebugToolbarExtension
    app.debug = True
    # make sure templates, etc. are not cached in debug mode
    app.jinja_env.auto_reload = app.debug

    connect_to_db(app)

    # Use the DebugToolbar
    # DebugToolbarExtension(app)

    app.run(port=5000, host='0.0.0.0')