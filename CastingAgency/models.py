from flask_sqlalchemy import SQLAlchemy
from sqlalchemy import Date, Column, String, Integer, create_engine
from datetime import datetime

db = SQLAlchemy()

database_name = "trivia"
database_path = "postgres://{}/{}".format('localhost:5432', database_name)

def setup_db(app):
    app.config["SQLALCHEMY_DATABASE_URI"] = database_path
    app.config["SQLALCHEMY_TRACK_MODIFICATIONS"] = False
    db.app = app
    db.init_app(app)
    db.create_all()

class Show(db.Model):
  __tablename__ = 'Shows'

  id = db.Column(db.Integer, primary_key=True)
  start_time = db.Column(db.Date, nullable=False) 
  actor_id = db.Column(db.Integer, db.ForeignKey('Actor.id'), nullable=False)
  movie_id = db.Column(db.Integer, db.ForeignKey('Movie.id'), nullable=False)

class Actor(db.Model):
    __tablename__ = 'Actor'

    id = db.Column(db.Integer, primary_key=True)
    name = db.Column(db.String)
    gender = db.Column(db.String)
    age = db.Column(db.Integer)
    shows = db.relationship('Show', backref='actor', lazy=True)


class Movie(db.Model):
    __tablename__ = 'Movie'

    id = db.Column(db.Integer, primary_key=True)
    title = db.Column(db.String)
    release_date = db.Column(db.Date)
    shows = db.relationship('Show', backref='movie', lazy=True)

