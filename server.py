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

    response = find_sg_events("Avett")

    return jsonify(response)





@app.route('/')
def index():
    """Homepage."""

    return render_template("homepage.html")


@app.route('/check_artist')
def check_artist():
    """List artists found that closely match artist entered by user."""
    
    artist_query = "Beyonce"

    # Call API for all artists closely matched, response is list of artist_sg_ids
    artist_sg_ids = list_artist_ids(artist_query)

    ## What happens when none found???

    ## If only one artist found, go directly to artist's page??
    print(artist_sg_ids)
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

    # Call API for all events of a particular artist, response is a list of event_sg_ids
    artist_sg_events = list_event_ids(artist_select.artist_sg_id)

    ## What happens when none found???
    ## Should never happen because of request argument has_upcoming_events set to True in check_artist request

    if artist_sg_events == "":
        return "Sorry"

    else:
        # Get each event object for each event_sg_id
        artist_events = [Event.query.filter(Event.event_sg_id == event).one() for event in artist_sg_events]

        artist_event_dicts = []
        
        for event in artist_events:

            eve = []

            eve.append(Event.query.filter(Event.event_id == event.event_id).one())

            event_artists = list_event_artists(event.event_id)

            art = {}

            for i, art_obj in enumerate(event_artists):

                art_obj = Artist.query.filter(Artist.artist_id == art_obj.artist_id).one()
                art['artist' + str(i + 1)] = art_obj

            eve.append(art)

            artist_event_dicts.append(eve)

        return render_template("artist.html", artist=artist_select, artist_event_dicts=artist_event_dicts)


@app.route('/check_venue')
def check_venue():
    """List events then list venues found that closely match event/venue entered by user."""
    user_query = "Greek"

    # Call API for all venues closely matched, response is list of venue_ids
    venue_sg_ids = list_venue_ids(user_query)

    ## What happens when none found???

    if venue_sg_ids != []:
        venue_options = [Venue.query.filter(Venue.venue_sg_id == venue).one() for venue in venue_sg_ids]
        return render_template("check_venue.html", venue_options=venue_options)

    else:
        return "Sorry"


@app.route('/venue/<venue_id>')
def display_venue(venue_id):
    """List all events for venue selected."""
    
    # Find venue object
    venue_select = Venue.query.filter(Venue.venue_id == venue_id).one()

    # Call API for all events for particular venue, response is list of event_ids
    venue_sg_events = list_venue_event_ids(venue_select.venue_sg_id)

    ## What happens when none found???

    if venue_sg_events == "":
        return "Sorry"

    else:
        venue_events = [Event.query.filter(Event.event_sg_id == event).one() for event in venue_sg_events]
        return render_template("venue.html", venue=venue_select, venue_events=venue_events)


@app.route('/check_event')
def check_event():
    """List events then list venues found that closely match event/venue entered by user."""
    user_query = "Avett"

    # Call API for all events closely matched, response is list of event_ids
    event_sg_ids = list_event_ids(user_query)

    ## What happens when none found???

    if event_sg_ids != []:
        event_options = [Event.query.filter(Event.event_sg_id == event).one() for event in event_sg_ids]
        return render_template("check_event.html", event_options=event_options)

    else:
        return "Sorry"


@app.route('/event/<event_id>')
def display_event(event_id):
    """Display event information."""
    
    # Find event object of event_id
    event_select = Event.query.filter(Event.event_id == event_id).one()

    event_sg_artists = list_event_artists(event_id)

    ## What happens when none found??? ## Maybe return page with just the event info and venue info??

    if event_sg_artists == "":
        return "Sorry"

    else:
        event_artists = [artist for artist in event_sg_artists]
        return render_template("event.html", event=event_select, event_artists=event_artists)




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