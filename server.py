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

    response = get_sg_venue(1291)

    return jsonify(response)





@app.route('/')
def index():
    """Homepage."""

    return render_template("homepage.html")


@app.route('/check_artist')
def check_artist(artist_input):
    """List artists found that closely match artist entered by user."""

    # Call API for all artists closely matched, response is list of artist_ids
    artist_options = find_sg_artists(artist_input)

    ## What happens when none found???
    
    # Add each artist to db if not already in db
    insert_artists(artist_options)
    
    return render_template("check_artist.html", artist_options=artist_options)


@app.route('/artist/<artist_id>')
def list_artist_events(artist_id):
    """List all events for artist entered."""

    # Find artist object of artist_id
    artist = Artist.query.filter(Artist.artist_id == artist_id).one()

    # Call API for all events of a particular artist, response is a list of artist_ids
    artist_events = find_artist_events(artist_id)

    ## What happens when none found???

    # Add each event to db if not already in db
    insert_events(artist_events)

    return render_template("artist_events.html", artist=artist, artist_events=artist_events)


@app.route('/check')
def check_venue_and_event(user_input):
    """List events then list venues found that closely match event/venue entered by user."""

    # Call API for all events closely matched, response is list of event_ids
    event_options = find_sg_events(user_input)

    ## What happens when none found???

    # Add event to db if not already in db
    insert_events(event_options)

    # Call API for all venues closely matched, response is list of venue_ids
    venue_options = find_sg_venues(user_input)

    ## What happens when none found???

    insert_venues(venue_options)
    
    return render_template("check.html", event_options=event_options, venue_options=venue_options)

 
@app.route('/venue/<venue_id>')
def list_venue_events(venue_id):
    """List all events for venue selected."""
    
    # Find venue object
    venue = Venue.query.filter(Venue.venue_id == venue_id).one()

    # Call API for all events for particular venue, response is list of event_ids
    venue_events = find_venue_events(venue_id)

    ## What happens when none found???

    insert_events(venue_events)

    return render_template("venue_events.html", venue=venue, venue_events=venue_events)


@app.route('/event/<event_id>')
def display_event(event_id):
    """Display event information."""
    
    # Find event object of event_id
    event = Event.query.filter(Event.event_id == event_id).one()

    event_artists = find_event_artists(event_id)

    ## What happens when none found???

    insert_events(event_artists)

    return render_template("event.html", event=event, artists=artists)


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