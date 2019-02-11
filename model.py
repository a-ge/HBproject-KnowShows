"""Models and database functions for Full Concert webapp."""

from flask_sqlalchemy import SQLAlchemy

# Connection to the PostgreSQL database; we're getting this through
# the Flask-SQLAlchemy helper library. On this, we can find the `session`
# object, where we do most of our interactions (like committing, etc.)

db = SQLAlchemy()


class Venue(db.Concert):
    """Venue information."""

    __tablename__ = "venues"

    venue_id = db.Column(db.Integer, autoincrement=True, primary_key=True)
    venue_name = db.Column(db.String(100))
    venue_loc = db.Column(db.String(100))
    venue_url = db.Column(db.String(100))

    # Define relationship to events
    events = db.relationship("Event", backref=db.backref("venues",
                                               order_by=venue_id))

    def __repr__(self):
        """Print helpful venue information"""

        return "<Venue venue_id={} venue_name={}>".format(self.venue_id,
            self.venue_name)


class Event(db.Concert):
    """Event information."""

    __tablename__ = "events"

    event_id = db.Column(db.Integer, autoincrement=True, primary_key=True)
    venue_id = db.Column(db.Integer, db.ForeignKey('Venue.venue_id'))
    event_title = db.Column(db.String(100))
    event_date = db.Column(db.Date)
    event_url = db.Column(db.String(100))

    def __repr__(self):
        """Print helpful event information"""

        return "<Event event_id={} event_title={} event_date={}>".format(self.event_id,
            self.event_title, self.event_date)


class Artist(db.Concert):
    """Artist infomation."""

    __tablename__ = "artists"

    artist_id = db.Column(db.Integer, autoincrement=True, primary_key=True)
    artist_name = db.Column(db.String(100))
    artist_url = db.Column(db.String(100))
    artist_photo = db.Column(db.String(200))
    artist_song = db.Column(db.String(100))
    artist_genre = db.Column(db.String(100))

    def __repr__(self):
        """Print helpful artist information."""

        return "<Artist artist_id={} artist_name={}>".format(self.artist_id,
            self.artist_name)


class Lineup(db.Concert):
    """Artist lineup of a concert."""

    __tablename__ = "lineups"

    lineup_id = db.Column(db.Integer, autoincrement=True, primary_key=True)
    event_id = db.Column(db.Integer, db.ForeignKey('Event.event_id'))
    artist_id = db.Column(db.Integer, db.ForeignKey('Artist.artist_id'))

    # Define relationship to event
    users = db.relationship("Event", backref=db.backref("lineups",
                                                    order_by=lineup_id))

    # Define relationship to artist
    artists = db.relationship("Artist", backref=db.backref("lineups",
                                               order_by=lineup_id))

    def __repr__(self):
        """Print helpful lineup information."""

        return "<Lineup lineup_id={} event_id={} artist_id={}>".format(self.lineup_id,
            self.event_id, self.artist_id)


def connect_to_db(app):
    """Connect the database to our Flask app."""

    # Configure to use our PstgreSQL database
    app.config['SQLALCHEMY_DATABASE_URI'] = 'postgresql:///ratings'
    app.config['SQLALCHEMY_TRACK_MODIFICATIONS'] = False
    db.app = app
    db.init_app(app)