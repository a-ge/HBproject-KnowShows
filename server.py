"""Concert Lineups."""

from jinja2 import StrictUndefined

from flask import (Flask, render_template, redirect, request, flash, session)

from flask_debugtoolbar import DebugToolbarExtension

from model import Event, Artist, Lineup, connect_to_db, db


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


@app.route('/<artist_id>')
def list_artist_events(artist_id):
    """Artist event details page."""

    # Find events that have lineups that match the artist_id
    artist_events = Event.query.filter(Lineup.artist_id == artist_id).all()
    # Find artist object of artist_id
    artist = Artist.query.filter(Artist.artist_id == artist_id).one()

    return render_template("artist_events.html", artist_events=artist_events, artist=artist)


@app.route('/check')
def check_venue_event():
    """List events then list venues found that closely match 
        event/venue entered by user."""


    return render_template("check.html")


@app.route('/<venue_id>')
def list_venue_events():
    """Venue event details page."""
    

    return render_template("venue_events.html")


@app.route('/<event_id>')
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