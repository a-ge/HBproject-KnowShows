"""View functions for Fill Concert webapp."""

from jinja2 import StrictUndefined

from flask import Flask, render_template, redirect, request, flash, session, jsonify

from flask_debugtoolbar import DebugToolbarExtension

from model import Event, Artist, Lineup, Venue, connect_to_db, db

from utility import *

app = Flask(__name__)

# Required to use Flask sessions and the debug toolbar
app.secret_key = "ABC"

# Normally, if you use an undefined variable in Jinja2, it fails
# silently. This is horrible. Fix this so that, instead, it raises an
# error.
app.jinja_env.undefined = StrictUndefined



@app.route('/test')
def test():

    response = find_artist_events(1768)

    return jsonify(response)





@app.route('/')
def index():
    """Homepage."""

    return render_template("homepage.html")


@app.route('/check_artist')
def check_artist():
    """List artists found that closely match artist entered by user."""
    
    artist_query = "Avett"

    # Call API for all artists closely matched, response is list of artist_sg_ids
    artist_sg_ids = list_artist_ids(artist_query)

    if artist_sg_ids != []:
        
        # Get each artist object for each artist_sg_id
        artist_options = [Artist.query.filter(Artist.artist_sg_id == artist).one() for artist in artist_sg_ids]

        return render_template("check_artist.html", artist_options=artist_options)
    else:

        return "Sorry"

@app.route('/artist/<artist_id>')
def list_artist_events(artist_id):
    """List all events for artist entered."""

    # Find artist object of artist_id
    artist_select = Artist.query.filter(Artist.artist_id == artist_id).one()

    # Call API for all events of a particular artist, response is a list of event_sg_ids
    artist_sg_events = list_event_ids(artist_select.artist_sg_id)

    ## What happens when none found???

    # Get each event object for each event_sg_id
    artist_events = [Event.query.filter(Event.event_sg_id == event).one() for event in artist_sg_events]

    return render_template("artist_events.html", artist=artist_select, artist_events=artist_events)


@app.route('/check')
def check_venue_and_event():
    """List events then list venues found that closely match event/venue entered by user."""
    user_query = "Avett"

    # Call API for all events closely matched, response is list of event_ids
    event_sg_ids = list_event_ids(user_query)

    event_options = [Event.query.filter(Event.event_sg_id == event).one() for event in event_sg_ids]
    ## What happens when none found???

    # Call API for all venues closely matched, response is list of venue_ids
    venue_sg_ids = list_venue_ids(user_query)

    venue_options = [Venue.query.filter(Venue.venue_sg_id == venue).one() for venue in venue_sg_ids]
    ## What happens when none found???
    
    return render_template("check.html", event_options=event_options, venue_options=venue_options)

 
@app.route('/venue/<venue_id>')
def list_venue_events(venue_id):
    """List all events for venue selected."""
    
    # Find venue object
    venue_select = Venue.query.filter(Venue.venue_id == venue_id).one()

    # Call API for all events for particular venue, response is list of event_ids
    venue_sg_events = list_venue_event_ids(venue_id)

    venue_events = [Event.query.filter(Event.event_sg_id == event).one() for event in venue_sg_events]
    ## What happens when none found???

    return render_template("venue_events.html", venue=venue_select, venue_events=venue_events)


@app.route('/event/<event_id>')
def display_event(event_id):
    """Display event information."""
    
    # Find event object of event_id
    event_select = Event.query.filter(Event.event_id == event_id).one()

    event_sg_artists = list_artist_ids(event_id)

    event_artists = [Artist.query.filter(Artist.artist_sg_id == artist).one() for artist in event_sg_artists]

    ## What happens when none found???

    return render_template("event.html", event=event_select, artists=artists)


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