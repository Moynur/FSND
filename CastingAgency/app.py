import os
from flask import Flask, request, abort, jsonify
from flask_sqlalchemy import SQLAlchemy
from flask_cors import CORS
from auth import *
from models import *

def create_app(test_config=None):
  
    app = Flask(__name__)
    setup_db(app)

    CORS(app, resources={r'/*': {'origins': '*'}})


    ## TODOS - get actors and movies
    @app.route('/actors', methods=['GET'])
    @requires_auth('read:actors')
    def get_actors(payload):
        try:
            actors = Actor.query.all()
            if len(actors) == 0:
              abort(404)
            return jsonify({
                'success': True,
                'actors': actors
              }), 200
        except:
          abort(401)

    @app.route('/movies', methods=['GET'])
    @requires_auth('read:movies')
    def get_movies(payload):
        try:
            movies = Movie.query.all()
            return jsonify({
            'success': True,
            'movies': movies
          }), 200
            if len(movies) == 0:
              abort(404)
        except:
              abort(422)

    ## TODOS - post actors and movies 

    @app.route('/actors', methods=['POST'])
    @requires_auth('create:actors')
    def create_actor(payload):
        body = request.get_json()
        try:
          new_actor = (Actor(
            name = body.get('name', None),
            age = body.get('age', None),
            gender = body.get('gender', None),
          )),
          new_actor.insert()
        except:
          abort(422)
        return jsonify({
          'success': True,
          'actor': new_actor
        }), 200

    @app.route('/movies', methods=['POST'])
    @requires_auth('create:movies')
    def create_movie(payload):
        body = request.get_json()
        try:
          new_movie = (Movie(
            name = body.get('name', None),
            age = body.get('age', None),
            gender = body.get('gender', None),
          )),
          new_movie.insert()
        except:
          abort(422)
    ## TODOS - delete actors and movies

    @app.route('/actors/<int:actor_id>', methods=['DELETE'])
    @requires_auth('delete:actors')
    def delete_actors(actor_id, payload):
        try:
          actor_delete = Actor.query.filter(Actor.id == actor_id).delete()
          return jsonify({
          'success': True,
          'deleted': actor_id
        }), 200
        except:
          abort(422)

    @app.route('/movies/<int:movie_id>', methods=['DELETE'])
    @requires_auth('delete:movies')
    def delete_movie(movie_id, payload):
        try:
          movie_delete = Movie.query.filter(Movie.id == movie_id).delete()
          return jsonify({
          'success': True,
          'deleted': movie_id
        }), 200
        except:
          abort(422)

      
    ## TODOS - patch actors and movies

    @app.route('/movies/<int:movie_id>', methods=['PATCH'])
    @requires_auth('edit:movies')
    def edit_movie(movie_id, payload):
        try:
          body = request.get_json()
          movie_update = Movie.query.filter(Movie.id == movie_id)
          movie_update.title = body.get('title', movie_update.title)
          movie_update.release_date = body.get('release_date', movie_update.release_date)
          movie_update.update()
          return jsonify({
          'success': True,
          'edited': movie_id
        }), 200
        except:
          abort(422)



    @app.route('/actors/edit/<actor_id>', methods=['PATCH'])
    @requires_auth('edit:actors')
    def edit_actor(actor_id, payload):
        try:
          body = request.get_json()
          actor_update = Actor.query.filter(Actor.id == actor_id)
          actor_update.name = body.get('name', actor_update.name)
          actor_update.age = body.get('age', actor_update.age)
          actor_update.gender = body.get('gender', actor_update.gender)
          actor_update.update()
          return jsonify({
          'success': True,
          'edited': movie_id
        }), 200
        except:
          abort(422)


    ## TODOS - error handlers

    @app.errorhandler(400)
    def bad_request(error):
        return jsonify({
                        "success": False, 
                        "error": 400,
                        "message": "bad request"
                        }), 400

    @app.errorhandler(401)
    def auth_fail(error):
        return jsonify({
                        "success": False, 
                        "error": 401,
                        "message": "authentification failed: unauthorized"
                        }), 401
                        
    @app.errorhandler(422)
    def unprocessable(error):
        return jsonify({
                        "success": False, 
                        "error": 422,
                        "message": "error processing request"
                        }), 422

    @app.errorhandler(404)
    def not_found(error):
        return jsonify({
                        "success": False, 
                        "error": 404,
                        "message": "resource not found"
                        }), 404                                      
    ## TODOS
    return app

app = create_app()

if __name__ == '__main__':
    app.run()