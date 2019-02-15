"""Concert Lineups."""

from jinja2 import StrictUndefined

from flask import (Flask, render_template, redirect, request, flash, session)

from flask_debugtoolbar import DebugToolbarExtension

from model import Event, Artist, Lineup, Venue, connect_to_db, db


app = Flask(__name__)

# Required to use Flask sessions and the debug toolbar
app.secret_key = "ABC"

# Normally, if you use an undefined variable in Jinja2, it fails
# silently. This is horrible. Fix this so that, instead, it raises an
# error.
app.jinja_env.undefined = StrictUndefined


@app.route('/')
def index():
    """Homepage."""

    return render_template("homepage.html")


@app.route('/check_artist')
def check_artist():
    """List artists found that closely match artist entered by user."""

    artist_input = 'Avett'

    # Need to check if found exact artist_name match???

    artist_options = Artist.query.filter(Artist.artist_name.like('%' + artist_input + '%')).all()

    return render_template("check_artist.html", artist_options=artist_options)


@app.route('/artist/<artist_id>')
def list_artist_events(artist_id):
    """List all events for artist selected."""

    # Find events that have lineups that match the artist_id
    artist_events = Event.query.filter(Lineup.artist_id == artist_id).all()
    # Find artist object of artist_id
    artist = Artist.query.filter(Artist.artist_id == artist_id).one()

    return render_template("artist_events.html", artist_events=artist_events, artist=artist)


@app.route('/check')
def check_venue_event():
    """List events then list venues found that closely match 
        event/venue entered by user."""

    check_input = 'UC'

    # Need to check if found exact event/venue match???

    event_options = Event.query.filter(Event.event_title.like('%' + check_input + '%')).all()
    venue_options = Venue.query.filter(Venue.venue_name.like('%' + check_input + '%')).all()
    print("******************************\n", venue_options)
    return render_template("check.html", event_options=event_options, venue_options=venue_options)


@app.route('/venue/<venue_id>')
def list_venue_events(venue_id):
    """Venue event details page."""
    
    # Find events for the venue_id
    venue_events = Event.query.filter(Event.venue_id == venue_id).all()
    # Find event object of venue_id
    venue = Venue.query.filter(Venue.venue_id == venue_id).one()

    return render_template("venue_events.html", venue_events=venue_events, venue=venue)


@app.route('/event/<event_id>')
def find_events():
    """List events based on date and location selected/entered by user."""
    

    return render_template("find_events.html")


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