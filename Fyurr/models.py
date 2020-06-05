from flask_sqlalchemy import SQLAlchemy

db = SQLAlchemy()

class Show(db.Model):
  __tablename__ = 'Shows'

  id = db.Column(db.Integer, primary_key=True)
  start_time = db.Column(db.DateTime(), nullable=False) 
  venue_id = db.Column(db.Integer, db.ForeignKey('Venue.id'), nullable=False)
  artist_id = db.Column(db.Integer, db.ForeignKey('Artist.id'), nullable=False)

class Venue(db.Model):
    __tablename__ = 'Venue'

    id = db.Column(db.Integer, primary_key=True)
    name = db.Column(db.String)
    city = db.Column(db.String(120))
    state = db.Column(db.String(120))
    address = db.Column(db.String(120))
    phone = db.Column(db.String(120))
    image_link = db.Column(db.String(500))
    facebook_link = db.Column(db.String(120))
    seeking_talent = db.Column(db.Boolean)
    shows = db.relationship('Show', backref='venue', lazy=True)
    genres = db.Column(db.String(120))
    description = db.Column(db.String(500))
    website = db.Column(db.String(300))


    def __repr__(self):
      return f'The {self.__class__.__name__} {self.name} is in {self.city}'

class Artist(db.Model):
    __tablename__ = 'Artist'

    id = db.Column(db.Integer, primary_key=True)
    name = db.Column(db.String)
    city = db.Column(db.String(120))
    state = db.Column(db.String(120))
    phone = db.Column(db.String(120))
    genres = db.Column(db.String(120))
    image_link = db.Column(db.String(500))
    facebook_link = db.Column(db.String(120))
    shows = db.relationship('Show', backref='artist', lazy=True)
    website = db.Column(db.String(300))

    def __repr__(self):
      return f'The {self.__class__.__name__} {self.name} is in {self.city}'
