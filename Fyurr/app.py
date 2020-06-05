#----------------------------------------------------------------------------#
# Imports
#----------------------------------------------------------------------------#

import json
import dateutil.parser
import babel
import sys
import datetime
from flask_moment import Moment
from flask_sqlalchemy import SQLAlchemy
import logging
from logging import Formatter, FileHandler
from flask_wtf import Form
from forms import *
from flask_migrate import Migrate
from datetime import datetime
from models import *
from flask import (
  Flask, 
  render_template, 
  request, 
  Response, 
  flash, 
  redirect, 
  url_for, 
  abort
)

#----------------------------------------------------------------------------#
# App Config.
#----------------------------------------------------------------------------#
app = Flask(__name__)
moment = Moment(app)
app.config.from_object('config')
#----------------------------------------------------------------------------#
# Models.
#----------------------------------------------------------------------------#
db.app = app
db.init_app(app)
Migrate(app, db)
migrate = Migrate(app, db)
#----------------------------------------------------------------------------#
# Filters.
#----------------------------------------------------------------------------#

def format_datetime(value, format='medium'):
  date = dateutil.parser.parse(value)
  if format == 'full':
      format="EEEE MMMM, d, y 'at' h:mma"
  elif format == 'medium':
      format="EE MM, dd, y h:mma"
  return babel.dates.format_datetime(date, format)

app.jinja_env.filters['datetime'] = format_datetime

#----------------------------------------------------------------------------#
# Controllers.
#----------------------------------------------------------------------------#

@app.route('/')
def index():
  return render_template('pages/home.html')

#  Venues
#  ----------------------------------------------------------------

@app.route('/venues')
def venues():
  venues_list = Venue.query.all()
  venues_dict = {}
  for venue in venues_list:
    key = f'{venue.city}, {venue.state}'

    venues_dict.setdefault(key, []).append({
        'id': venue.id,
        'name': venue.name,
        'num_upcoming_shows': len(venue.shows),
        'city': venue.city,
        'state': venue.state
      })

  data = []
  for value in venues_dict.values():
      data.append({
        'city': value[0]['city'],
        'state': value[0]['state'],
        'venues': value
      })

  return render_template('pages/venues.html', areas=data)

@app.route('/venues/search', methods=['POST'])
def search_venues():
  search_term = '%{}%'.format(request.form.get('search_term').lower())
  search_result = Venue.query.filter(Venue.name.ilike(search_term)).all()
  results = {}
  results["data"] = []
  results["count"] = len(search_result)
  for x in search_result:
    results.get("data").append({
      "id": x.id,
      "name": x.name,
    })
  return render_template('pages/search_venues.html', results=results, search_term=request.form.get('search_term', ''))

@app.route('/venues/<int:venue_id>')
def show_venue(venue_id):
  venue = Venue.query.filter(Venue.id==venue_id).first()
  shows = Show.query.filter(Show.venue_id==venue_id).all()
  past_shows = []
  upcoming_shows = []
  data = {}
  if venue is None:
    return not_found_error('Venue not found')
  for x in shows: 
    if x.start_time >= datetime.now():
      upcoming_shows.append({
        "artist_id": x.artist_id,
        "artist_name": Artist.query.filter(Artist.id == x.artist_id).first().name,
        "artist_image_link": Artist.query.filter(Artist.id == x.artist_id).first().image_link,
        "start_time": x.start_time.strftime('%m/%d/%y'),
      })
    else:
      past_shows.append({
        "artist_id": x.artist_id,
        "artist_name": Artist.query.filter(Artist.id == x.artist_id).first().name,
        "artist_image_link": Artist.query.filter(Artist.id == x.artist_id).first().image_link,
        "start_time":  x.start_time.strftime('%m/%d/%y'),
      }) 
  venueinfo = {
      'id': venue.id,
      "name": venue.name,
      "address": venue.address,
      "city":  venue.city,
      "state": venue.state,
      "phone": venue.phone,
      "website": venue.website,
      "facebook_link": venue.facebook_link,
      "seeking_talent": venue.seeking_talent,
      "seeking_description": venue.description,
      "image_link": venue.image_link,
      "past_shows": past_shows,
      "upcoming_shows": upcoming_shows,
      "past_shows_count": Show.query.filter(venue_id == Show.venue_id, Show.start_time < datetime.now()).count(),
      "upcoming_shows_count": Show.query.filter(venue_id == Show.venue_id, Show.start_time >= datetime.now()).count(),
      "genres": venue.genres.split(','),
  }
  return render_template('pages/show_venue.html', venue=venueinfo)

#  Create Venue
#  ----------------------------------------------------------------

@app.route('/venues/create', methods=['GET'])
def create_venue_form():
  form = VenueForm()
  return render_template('forms/new_venue.html', form=form)

@app.route('/venues/create', methods=['POST'])
def create_venue_submission():
  error = False
  body = {}
  try:
    name = request.form['name']
    city = request.form['city']
    state = request.form['state']
    address = request.form['address']
    phone = request.form['phone']
    facebook_link= request.form['facebook_link']
    genre = request.form.getlist('genres')
    venue_submission = Venue(name=name, city=city, state=state, address=address, phone=phone, 
    facebook_link=facebook_link, genres = genre)
    db.session.add(venue_submission)
    db.session.commit()
    body['name'] = venue_submission.name
  except:
    error = True
    db.session.rollback()
    print(sys.exc_info())
  finally:
    db.session.close()
  if error:
    flash('Add venue ' + request.form['name'] + ' failed!')
    abort (400)
  else:
    flash('Venue ' + request.form['name'] + ' was successfully listed!')
  return render_template('pages/home.html')

@app.route('/venues/<venue_id>', methods=['POST'])
def delete_venue(venue_id):
  try:
    venue = Venue.query.get(venue_id)
    db.dession.delete(venue)
    db.session.commit()
  except:
    db.session.rollback()
    print(sys.exc_info())
    flash('An error occurred. Venue '  + venue_id + ' could not be deleted.')
  finally:
    db.session.close()
  return  render_template(url_for('pages/home.html'))

  # BONUS CHALLENGE: Implement a button to delete a Venue on a Venue Page, have it so that 
  # clicking that button delete it from the db then redirect the user to the homepage 

#  Artists
#  ----------------------------------------------------------------
@app.route('/artists')
def artists():
  artists = Artist.query.all()
  artist = []
  try:
    for x in artists:
      artist.append({
        "id": x.id,
        "name":x.name
      })   
  except:
    flash('An error occurred')
  return render_template('pages/artists.html', artists=artist)

@app.route('/artists/search', methods=['POST'])
def search_artists():
  search_term = '%{}%'.format(request.form.get('search_term').lower())
  search_result = Artist.query.filter(Artist.name.ilike(search_term)).all()
  results = {}
  results["data"] = []
  results["count"] = len(search_result)
  for x in search_result:
    results.get("data").append({
      "id": x.id,
      "name": x.name,
    })
  return render_template('pages/search_venues.html', results=results, search_term=request.form.get('search_term', ''))
  return render_template('pages/search_artists.html', results=response, search_term=request.form.get('search_term', ''))

@app.route('/artists/<int:artist_id>')
def show_artist(artist_id):
  artist = Artist.query.filter(Artist.id==artist_id).first()
  shows = Show.query.filter(Show.artist_id==artist_id).all()
  past_shows = []
  upcoming_shows = []
  data = {}
  if artist is None:
    return not_found_error('Venue not found')
  for x in shows: 
    if x.start_time >= datetime.now():
      upcoming_shows.append({
        "artist_id": x.artist_id,
        "artist_name": Artist.query.filter(Artist.id == x.artist_id).first().name,
        "artist_image_link": Artist.query.filter(Artist.id == x.artist_id).first().image_link,
        "start_time": x.start_time.strftime('%m/%d/%y'),
      })
    else:
      past_shows.append({
        "artist_id": x.artist_id,
        "artist_name": Artist.query.filter(Artist.id == x.artist_id).first().name,
        "artist_image_link": Artist.query.filter(Artist.id == x.artist_id).first().image_link,
        "start_time":  x.start_time.strftime('%m/%d/%y'),
      }) 
  artistinfo = {
        "id": artist.id,
        "name": artist.name,
        "genres": artist.genres.split(','),
        "city":  artist.city,
        "state": artist.state,
        "phone": artist.phone,
        "website": artist.website,
        "facebook_link": artist.facebook_link,
        "image_link": artist.image_link,
        "past_shows": past_shows,
        "upcoming_shows": upcoming_shows,
        "past_shows_count": Show.query.filter(artist_id == Show.artist_id, Show.start_time < datetime.now()).count(),
        "upcoming_shows_count": Show.query.filter(artist_id == Show.artist_id, Show.start_time >= datetime.now()).count(),
  }
  return render_template('pages/show_artist.html', artist=artistinfo)

#  Update
#  ----------------------------------------------------------------
@app.route('/artists/<int:artist_id>/edit', methods=['GET'])
def edit_artist(artist_id):
  form = ArtistForm()
  user = Artist.query.get(artist_id)
  if user is None:
    return not_found_error('User does not found')
  artist={
    "id": user.id,
    "name": user.name,
    "genres": user.genres.split(','),
    "city":  user.city,
    "state": user.state,
    "phone": user.phone,
    "website": user.website,
    "facebook_link": user.facebook_link,
    "image_link": user.image_link
  }
  return render_template('forms/edit_artist.html', form=form, artist=artist)

@app.route('/artists/<int:artist_id>/edit', methods=['POST'])
def edit_artist_submission(artist_id):
  user = Artist.query.get(artist_id)
  if user is None:
     return not_found_error('Artist not found')
  try:
    user.name = request.form.get('name')
    user.city = request.form.get('city')
    user.state = request.form.get('state')
    user.phone = request.form.get('phone')
    user.facebook_link = request.form.get('facebook_link')
    user.genres = ','.join(request.form.getlist('genres'))
    db.session.commit()
  except:
    print('An error occurred Artist ' + request.form.get('name') + ' could not be updated.') 
    db.session.rollback()
  finally:
    db.session.close()
  return redirect(url_for('show_artist', artist_id=artist_id))

@app.route('/venues/<int:venue_id>/edit', methods=['GET'])
def edit_venue(venue_id):
  form = VenueForm()
  user = Venue.query.get(artist_id)
  if user is None:
    return not_found_error('Venue not found')
  venue={
    "id": user.id,
    "name": user.name,
    "genres": user.genres.split(','),
    "city":  user.city,
    "state": user.state,
    "phone": user.phone,
    "website": user.website,
    "facebook_link": user.facebook_link,
    "seeking_venue": user.seeking_talent,
    "seeking_description": user.seeking_description,
    "image_link": user.image_link
  }
  return render_template('forms/edit_venue.html', form=form, venue=venue)


@app.route('/venues/<int:venue_id>/edit', methods=['POST'])
def edit_venue_submission(venue_id):
  user = Venue.query.get(artist_id)
  if user is None:
     return not_found_error('Venue not found')
  try:
    user.name = request.form.get('name')
    user.city = request.form.get('city')
    user.state = request.form.get('state')
    user.phone = request.form.get('phone')
    user.facebook_link = request.form.get('facebook_link')
    user.genres = ','.join(request.form.getlist('genres'))
    db.session.commit()
  except:
    print('An error occurred Venue ' + request.form.get('name') + ' could not be updated.') 
    db.session.rollback()
  finally:
    db.session.close()
  return redirect(url_for('show_venue', venue_id=venue_id))

#  Create Artist - request info
#  ----------------------------------------------------------------

@app.route('/artists/create', methods=['GET'])
def create_artist_form():
  form = ArtistForm()
  return render_template('forms/new_artist.html', form=form)

#  ----------------------------------------------------------------
#  Create Artist - Commit do db
@app.route('/artists/create', methods=['POST'])
def create_artist_submission():
  try:
    name = request.form.get('name')
    city = request.form.get('city')
    state = request.form.get('state')
    phone = request.form.get('phone')
    facebook_link = request.form.get('facebook_link')
    genres = request.form.getlist('genres')
    artist = Artist(name=name, city=city, state=state,
    phone=phone, facebook_link=facebook_link, genres=','.join(genres))
    db.session.add(artist)
    db.session.commit()
    flash('Artist ' + request.form['name'] + ' was successfully listed!')
  except:
    db.session.rollback() 
    flash('An error occurred. Artist ' + request.form.get('name') + ' could not be listed.')
  finally:
    db.session.close()
  return render_template('pages/home.html')


#  Shows
#  ----------------------------------------------------------------

@app.route('/shows')
def shows():
  data=[]
  for show in Show.query.all():
    data.append({
      "venue_id": show.venue_id,
      "venue_name": Venue.query.filter(Venue.id == show.venue_id).first().name,
      "artist_id": show.artist_id,
      "artist_name": show.artist.name,
      "artist_image_link": show.artist.image_link,
      "start_time": show.start_time.strftime("%d/%m/%Y, %H:%M:%S"),
    })
  return render_template('pages/shows.html', shows=data)
#  ----------------------------------------------------------------
@app.route('/shows/create')
def create_shows():
  # renders form. do not touch.
  form = ShowForm()
  return render_template('forms/new_show.html', form=form)
#  ----------------------------------------------------------------
# commit new show to db
@app.route('/shows/create', methods=['POST'])
def create_show_submission():
  try:
      artist_id = request.form.get('artist_id')
      venue_id = request.form.get('venue_id')
      start_time = request.form.get("start_time")
      newShow = Show(artist_id = artist_id, venue_id = venue_id, start_time= start_time)
      db.session.add(newShow)
      db.session.commit()
      flash('Show was successfully listed!')
  except:
      db.session.rollback()
      flash('An error occurred. Show could not be listed.')
      print(sys.exc_info()) 
  finally:
      db.session.close()
  return render_template('pages/home.html')
  flash('Show was successfully listed!')

# --------------------------------------------------
# Error handlers   
@app.errorhandler(404)
def not_found_error(error):
    return render_template('errors/404.html'), 404

@app.errorhandler(500)
def server_error(error):
    return render_template('errors/500.html'), 500


if not app.debug:
    file_handler = FileHandler('error.log')
    file_handler.setFormatter(
        Formatter('%(asctime)s %(levelname)s: %(message)s [in %(pathname)s:%(lineno)d]')
    )
    app.logger.setLevel(logging.INFO)
    file_handler.setLevel(logging.INFO)
    app.logger.addHandler(file_handler)
    app.logger.info('errors')

#----------------------------------------------------------------------------#
# Launch.
#----------------------------------------------------------------------------#

# Default port:
if __name__ == '__main__':
    app.run()

# Or specify port manually:
'''
if __name__ == '__main__':
    port = int(os.environ.get('PORT', 5000))
    app.run(host='0.0.0.0', port=port)
'''
