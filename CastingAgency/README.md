# Capstone API

## Getting Started

### Installing Dependencies

#### Python 3.7

Follow instructions to install the latest version of python for your platform in the [python docs](https://docs.python.org/3/using/unix.html#getting-and-installing-the-latest-version-of-python)

#### Virtual Enviornment

We recommend working within a virtual environment whenever using Python for projects. This keeps your dependencies for each project separate and organaized. Instructions for setting up a virual enviornment for your platform can be found in the [python docs](https://packaging.python.org/guides/installing-using-pip-and-virtual-environments/)

#### PIP Dependencies

Once you have your virtual environment setup and running, install dependencies by naviging to the `/backend` directory and running:

```bash
pip install -r requirements.txt
```

This will install all of the required packages we selected within the `requirements.txt` file.

###### Host URLs

https://moynurcapstone1.herokuapp.com/ | https://git.heroku.com/moynurcapstone1.git

##### Key Dependencies

- [Flask](http://flask.pocoo.org/)  is a lightweight backend microservices framework. Flask is required to handle requests and responses.

- [SQLAlchemy](https://www.sqlalchemy.org/) is the Python SQL toolkit and ORM we'll use handle the lightweight sqlite database. You'll primarily work in app.py and can reference models.py. 

- [Flask-CORS](https://flask-cors.readthedocs.io/en/latest/#) is the extension we'll use to handle cross origin requests from our frontend server. 


'/movies' GET
- gets all movies in db 
Reponse:

 {"movies": [
    {
      "id": 1,
      "release_date": "2020-01-01",
      "title": "Title"
    },
    {
      "id": 2,
      "release_date": "2020-01-01",
      "title": "Title"
    }
  ]
}

'/movies' Post
Add new movie to db
Entry
{
  "title": "title",
  "release_date": "release_date"
}
Response:
{
  'success': true,
  'movie': 'title'
}

'/movies/<int:movie_id> Patch
edit movie entry
Entry
{
  "title": "new title",
  "release_date": "2020-01-01"
}

{
  'success': true,
  'movie': {
              "id": 1,
              "release_date": "2020-01-01",
              "title": "new title"
            }
}

'movies/<int:movie_id> Delete
Delete a movie from db 
{
  'success': true,
  'delete': 1
}

Actors Endpoints:
'/actors' GET
- gets all actors in db 
Reponse:

 {"actors": [
    {
      "id": 1,
      "name": "Name",
      "gender": "M"
    },
    {
      "id": 2,
      "name": "Name2",
      "gender": "F"
    }
  ]
}

'/actors' Post
Add new movie to db
Entry
{
  "name": "name",
  "gender": "F"
}
Response:
{
  'success': true,
  'name': 'name'
}

'/actors/<int:actor_id> Patch
edit actor entry
Entry
{
  "name": "new name",
  "gender": "M"
}

{
  'success': true,
  'movie': {
              "id": 1,
              "gender": "M",
              "name": "name"
            }
}

'actors/<int:actor_id> Delete
Delete an actor from db 
{
  'success': true,
  'delete': 1
}

Errors: 
Failed to process request 422
        "success": False,
        "error": 422,
        "message": "Unprocessable"
      }), 422

Not Found 404
        "success": False,
        "error": 404,
        "message": "Resource not found"
      }), 404

Bad Request 400
        "success": False,
        "error": 400,
        "message": "Bad Request"
      }), 400

Server error 500
        "success": False,
        "error": 500,
        "message": "Bad Request"
      }), 500


## Testing
To run the tests, run
```
python test_app.py
```