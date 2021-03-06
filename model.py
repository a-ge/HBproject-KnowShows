"""Models for KnowShows webapp."""

from flask_sqlalchemy import SQLAlchemy

from datetime import datetime

# Connection to the PostgreSQL database; we're getting this through
# the Flask-SQLAlchemy helper library. On this, we can find the `session`
# object, where we do most of our interactions (like committing, etc.)

db = SQLAlchemy()



class Venue(db.Model):
    """Venue information."""

    __tablename__ = "venues"

    venue_id = db.Column(db.Integer, autoincrement=True, primary_key=True)
    venue_sg_id = db.Column(db.Integer, unique=True)
    venue_name = db.Column(db.String(100))
    venue_add = db.Column(db.String(100))
    venue_city = db.Column(db.String(100))
    venue_state = db.Column(db.String(100))
    venue_zip = db.Column(db.String(1000))

    def __repr__(self):
        """Print helpful venue information"""

        return "<Venue venue_id={} venue_name={}>".format(self.venue_id,
            self.venue_name)


class Event(db.Model):
    """Event information."""

    __tablename__ = "events"

    event_id = db.Column(db.Integer, autoincrement=True, primary_key=True)
    venue_id = db.Column(db.Integer, db.ForeignKey('venues.venue_id'))
    event_sg_id = db.Column(db.Integer, unique=True)
    event_title = db.Column(db.String(500))
    event_datetime = db.Column(db.String(100))
    event_url = db.Column(db.String(1000))
    event_sp_playlist_id = db.Column(db.String(100), nullable=True)

    # Define relationship to venue
    venue = db.relationship("Venue", backref="events")

    def __repr__(self):
        """Print helpful event information"""

        return "<Event event_id={} event_title={} event_datetime={}>".format(self.event_id,
            self.event_title, self.event_datetime)


class Lineup(db.Model):
    """Artist lineup of a concert."""

    __tablename__ = "lineups"

    lineup_id = db.Column(db.Integer, autoincrement=True, primary_key=True)
    event_id = db.Column(db.Integer, db.ForeignKey('events.event_id'))
    artist_id = db.Column(db.Integer, db.ForeignKey('artists.artist_id'))

    # Define relationship to event
    event = db.relationship("Event", backref="lineups")

    # Define relationship to artist
    artist = db.relationship("Artist", backref="lineups")

    def __repr__(self):
        """Print helpful lineup information."""

        return "<Lineup lineup_id={} event_id={} artist_id={}>".format(self.lineup_id,
            self.event_id, self.artist_id)


class Artist(db.Model):
    """Artist infomation."""

    __tablename__ = "artists"

    artist_id = db.Column(db.Integer, autoincrement=True, primary_key=True)
    spotify_uri = db.Column(db.String(200))
    artist_sp_playlist_id = db.Column(db.String(100), nullable=True)
    artist_sg_id = db.Column(db.Integer, unique=True)
    artist_name = db.Column(db.String(100))
    artist_url = db.Column(db.String(1000))
    artist_photo = db.Column(db.String(1000))
    artist_genres = db.Column(db.String(200))
    artist_bio = db.Column(db.String(2000), nullable=True)

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