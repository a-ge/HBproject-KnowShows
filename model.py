"""Models and database functions for Full Concert webapp."""

from flask_sqlalchemy import SQLAlchemy

# Connection to the PostgreSQL database; we're getting this through
# the Flask-SQLAlchemy helper library. On this, we can find the `session`
# object, where we do most of our interactions (like committing, etc.)

db = SQLAlchemy()


class Venue(db.Model):
    """Venue information."""

    __tablename__ = "venues"

    venue_id = db.Column(db.Integer, autoincrement=True, primary_key=True)
    venue_name = db.Column(db.String(100))
    venue_loc = db.Column(db.String(100))
    venue_url = db.Column(db.String(200))

    # Define relationship to events
    events = db.relationship("Event", backref=db.backref("venues"))

    def __repr__(self):
        """Print helpful venue information"""

        return "<Venue venue_id={} venue_name={}>".format(self.venue_id,
            self.venue_name)


class Event(db.Model):
    """Event information."""

    __tablename__ = "events"

    event_id = db.Column(db.Integer, autoincrement=True, primary_key=True)
    venue_id = db.Column(db.Integer, db.ForeignKey('venues.venue_id'))
    event_title = db.Column(db.String(100))
    event_date = db.Column(db.Date)
    event_url = db.Column(db.String(200))

    def __repr__(self):
        """Print helpful event information"""

        return "<Event event_id={} event_title={} event_date={}>".format(self.event_id,
            self.event_title, self.event_date)


class Lineup(db.Model):
    """Artist lineup of a concert."""

    __tablename__ = "lineups"

    lineup_id = db.Column(db.Integer, autoincrement=True, primary_key=True)
    event_id = db.Column(db.Integer, db.ForeignKey('events.event_id'))
    artist_id = db.Column(db.Integer, db.ForeignKey('artists.artist_id'))

    # Define relationship to event
    users = db.relationship("Event", backref=db.backref("lineups"))

    # Define relationship to artist
    artists = db.relationship("Artist", backref=db.backref("lineups"))

    def __repr__(self):
        """Print helpful lineup information."""

        return "<Lineup lineup_id={} event_id={} artist_id={}>".format(self.lineup_id,
            self.event_id, self.artist_id)


class Artist(db.Model):
    """Artist infomation."""

    __tablename__ = "artists"

    artist_id = db.Column(db.Integer, autoincrement=True, primary_key=True)
    spotify_id = db.Column(db.String(100))
    ticket_id = db.Column(db.Integer)
    artist_name = db.Column(db.String(100))
    artist_url = db.Column(db.String(200))
    artist_photo = db.Column(db.String(200))
    artist_song = db.Column(db.String(100))
    artist_genre = db.Column(db.String(100))

    def __repr__(self):
        """Print helpful artist information."""

        return "<Artist artist_id={} artist_name={}>".format(self.artist_id,
            self.artist_name)



def connect_to_db(app):
    """Connect the database to our Flask app."""

    # Configure to use our PstgreSQL database
    app.config['SQLALCHEMY_DATABASE_URI'] = 'postgresql:///concerts'
    app.config['SQLALCHEMY_TRACK_MODIFICATIONS'] = False
    db.app = app
    db.init_app(app)


if __name__ == "__main__":
    # As a convenience, if we run this module interactively, it will leave
    # you in a state of being able to work with the database directly.

    from server import app
    connect_to_db(app)
    print("Connected to DB.")