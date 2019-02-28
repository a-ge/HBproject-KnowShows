"""View functions for Full Concert webapp."""

from jinja2 import StrictUndefined
from flask import Flask, render_template, redirect, request, flash, session, jsonify
from flask_debugtoolbar import DebugToolbarExtension

from model import Event, Artist, Lineup, Venue, connect_to_db, db
from utility import *

# For testing with /test
from utility_spotify import *

app = Flask(__name__)

# Required to use Flask sessions and the debug toolbar
app.secret_key = "ABC"

# Normally, if you use an undefined variable in Jinja2, it fails silently.
# This is horrible. Fix this so that, instead, it raises an error.
app.jinja_env.undefined = StrictUndefined



@app.route('/test')
def test():

    response = create_playlist(["196lKsA13K3keVXMDFK66q"])

    return response.text




@app.route('/', methods=["GET", "POST"])
def index():
    """Homepage."""

    # if request.method == "POST":
    #     session['lat'] = request.json['lat']
    #     session['lng'] = request.json['lng']
    # else:
    #     session['lat'] = None
    #     session['lng'] = None


    return render_template("homepage.html")


@app.route('/search', methods=['POST'])
def search():
    """ Retrieve user's search inputs and redirect to correct page."""

    ## Check if key exists and if they do, pop out OR
    # if session:
    #     for key in session.keys():
    #      session.pop(key)

    if request.method == "POST":

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

    # start_date = '2019-03-21'
    # end_date = '2019-03-23'

    if query_type == "Artist":
        return redirect("/check_artist")

    elif query_type == "Venue":
        return redirect("/check_venue")

    elif query_type == "Event":
        return redirect("/check_event")


@app.route('/check_artist')
def check_artist():
    """List artists found that closely match artist entered by user."""

    # Search db, then if necessary, call API for artists, response is a list of artist_sg_ids
        ## Currently have request argument has_upcoming_events set to True
        ## This means artists with no upcoming events will not appear --change?? create flash message??
    artist_sg_ids = list_artist_ids(session['user_query'])

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

    # Search db, then if necessary, call API for venues, response is a list of venue_sg_ids
        ## The Greek Berkeley has a few venue_ids, how to correct this??
        ## Still import a venue if they have no upcoming events??
    venue_sg_ids = list_venue_ids(session['user_query'])

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

    # Search db, then if necessary, call API for events, response is a list of event_sg_ids
    event_sg_ids = list_event_ids(session['user_query'])

    ## What happens when none found???

    if event_sg_ids != []:
        # Get each event object for each event_sg_id
        event_options = [Event.query.filter(Event.event_sg_id == event).one() for event in event_sg_ids]
        return render_template("check_event.html", event_options=event_options)

    else:
        return "Sorry"


@app.route('/event/<event_id>')
def display_event(event_id):
    """Display event information."""
    
    # Find event object of event_id
    event_select = Event.query.filter(Event.event_id == event_id).one()

    ## What happens when none found??? ## Maybe return page with just the event info and venue info??

    event_dicts = list_event_artists(event_id)

    artist_spot_ids = [value.spotify_uri for key, value in event_dicts.items()]

    playlist_id = create_playlist(artist_spot_ids)

    return render_template("event.html", event=event_select, event_dicts=event_dicts, playlist_id=playlist_id)




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