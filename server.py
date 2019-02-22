"""View functions for Full Concert webapp."""

from jinja2 import StrictUndefined
from flask import Flask, render_template, redirect, request, flash, session, jsonify
from flask_debugtoolbar import DebugToolbarExtension

from model import Event, Artist, Lineup, Venue, connect_to_db, db
from utility import *


app = Flask(__name__)

# Required to use Flask sessions and the debug toolbar
app.secret_key = "ABC"

# Normally, if you use an undefined variable in Jinja2, it fails silently.
# This is horrible. Fix this so that, instead, it raises an error.
app.jinja_env.undefined = StrictUndefined



@app.route('/test')
def test():

    response = find_venue_events(1291)

    return jsonify(response)





@app.route('/')
def index():
    """Homepage."""


    return render_template("homepage.html")

@app.route('/search')
def search():

    user_query = request.args.get('userSearchInput')
    city = request.args.get('userCityInput')
    query_type = request.args.get('searchType')
    print("*************", user_query, city, query_type)

    if query_type == "Artist":
        return render_template("check_artist.html", user_query=user_query, city=city)

    elif query_type == "Venue":
        return render_template("check_venue.html", user_query=user_query, city=city)

    elif query_type == "Event":
        return render_template("check_event.html", user_query=user_query, city=city)

@app.route('/check_artist')
def check_artist():
    """List artists found that closely match artist entered by user."""
    
    artist_query = "Avett"

    # Search db, then if necessary, call API for artists, response is a list of artist_sg_ids
        ## Currently have request argument has_upcoming_events set to True
        ## This means artists with no upcoming events will not appear --change?? create flash message??
    artist_sg_ids = list_artist_ids(artist_query)

    ## What happens when none found???

    ## If only one artist found, go directly to artist's page??

    if artist_sg_ids != []:
        # Get each artist object for each artist_sg_id
        artist_options = [Artist.query.filter(Artist.artist_sg_id == artist).one() for artist in artist_sg_ids]
        return render_template("check_artist.html", artist_options=artist_options)

    else:
        return "Sorry"


@app.route('/artist/<artist_id>')
def display_artist(artist_id):
    """List all events with their lineup artists for artist selected."""

    # Find artist object of artist_id
    artist_select = Artist.query.filter(Artist.artist_id == artist_id).one()

    # Search db, then if necessary, call API for all events of a particular artist, response is a list of event_sg_ids
    artist_sg_events = list_event_ids(artist_select.artist_sg_id)

    ## What happens when none found???

    if artist_sg_events != "":
        # Create a list with nested lists where event obj in index 0
        # and following indexes are the artist objs for given event
        artist_event_dicts = []
        
        for event in artist_sg_events:

            eve = []

            eve_obj = Event.query.filter(Event.event_sg_id == event).one()

            # First add event object 
            eve.append(eve_obj)

            # Get dictionary with each artist object
            eve.append(list_event_artists(eve_obj.event_id))

            artist_event_dicts.append(eve)

        return render_template("artist.html", artist=artist_select, artist_event_dicts=artist_event_dicts)

    else:
        return "Sorry"


@app.route('/check_venue')
def check_venue():
    """List venues found that closely match venue entered by user."""

    user_query = "Greek"

    # Search db, then if necessary, call API for venues, response is a list of venue_sg_ids
    venue_sg_ids = list_venue_ids(user_query)

    ## What happens when none found???

    if venue_sg_ids != []:
        # Get each venue object for each venue_sg_id
        venue_options = [Venue.query.filter(Venue.venue_sg_id == venue).one() for venue in venue_sg_ids]
        return render_template("check_venue.html", venue_options=venue_options)

    else:
        return "Sorry"


@app.route('/venue/<venue_id>')
def display_venue(venue_id):
    """List all events with lineups artists for venue selected."""
    
    # Find venue object
    venue_select = Venue.query.filter(Venue.venue_id == venue_id).one()

    # Search db, then if necessary, call API for venues, response is a list of venue_sg_ids
    venue_sg_events = list_venue_event_ids(venue_select.venue_sg_id)

    ## What happens when none found???

    if venue_sg_events != "":

        venue_event_dicts = []
        
        for event in venue_sg_events:

            eve = []

            eve_obj = Event.query.filter(Event.event_sg_id == event).one()

            # First add event object 
            eve.append(eve_obj)

            # Get a list with each artist object
            eve.append(list_event_artists(eve_obj.event_id))

            venue_event_dicts.append(eve)

        return render_template("venue.html", venue=venue_select, venue_event_dicts=venue_event_dicts)

    else:
        return "Sorry"


@app.route('/check_event')
def check_event():
    """List events found that closely match event entered by user."""

    user_query = "festival"

    # Search db, then if necessary, call API for events, response is a list of event_sg_ids
    event_sg_ids = list_event_ids(user_query)

    ## What happens when none found???

    if event_sg_ids != []:
        # Get each event object for each event_sg_id
        event_options = [Event.query.filter(Event.event_sg_id == event).one() for event in event_sg_ids]
        return render_template("check_event.html", event_options=event_options)

    else:
        return "Sorry"



@app.route('/suggest_event')
def suggest_event():


    return render_template("event_options.html", event_options=event_options)



@app.route('/event/<event_id>')
def display_event(event_id):
    """Display event information."""
    
    # Find event object of event_id
    event_select = Event.query.filter(Event.event_id == event_id).one()

    ## What happens when none found??? ## Maybe return page with just the event info and venue info??

    event_dicts = list_event_artists(event_id)

    return render_template("event.html", event=event_select, event_dicts=event_dicts)




if __name__ == "__main__":
    # We have to set debug=True here, since it has to be True at the
    # point that we invoke the DebugToolbarExtension
    app.debug = True
    # make sure templates, etc. are not cached in debug mode
    app.jinja_env.auto_reload = app.debug

    connect_to_db(app)

    # Use the DebugToolbar
    DebugToolbarExtension(app)

    app.run(port=5000, host='0.0.0.0')