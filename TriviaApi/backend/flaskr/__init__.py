#----------------------------------------------------------------------------#
# Imports
#----------------------------------------------------------------------------#
import os
from flask import Flask, request, abort, jsonify, json
from flask_sqlalchemy import SQLAlchemy
from flask_cors import CORS
import random

from models import setup_db, Question, Category

QUESTIONS_PER_PAGE = 10

#  Setup
#  ----------------------------------------------------------------

def create_app():
    """
    @TODO: Set up CORS. Allow '*' for origins. Delete the sample route after completing the TODOs
    """
    app = Flask(__name__)
    setup_db(app)

    CORS(app, resources={r'/*': {'origins': '*'}})

    @app.after_request
    def set_headers(response):
        """
        @TODO: Use the after_request decorator to set Access-Control-Allow
        """
        response.headers.add('Access-Control-Allow-Headers',
                             'Content-Type, Authorization, true')
        response.headers.add('Access-Control-Allow-Methods',
                             'GET, PATCH, POST, DELETE, OPTIONS')
        return response

    @app.route('/categories', methods=['GET'])
    def get_all_categories():
        """
          Create an endpoint to handle GET requests 
          for all available categories.
        """
        categories = {}
        for category in Category.query.all():
            categories[category.id] = category.type
        return jsonify({
            'categories': categories
        })
#  Get Questions - working
#  ----------------------------------------------------------------
    @app.route('/questions', methods=['GET'])
    def get_questions():
        categories = {}
        for category in Category.query.all():
            categories[category.id] = category.type
        questions = [question.format() for question in Question.query.all()]
        page = int(request.args.get('page', '0'))
        upper_limit = page * 10
        lower_limit = upper_limit - 10
        return jsonify({
            'questions': questions[
                         lower_limit:upper_limit] if page else questions,
            'total_questions': len(questions),
            'categories': categories
        })
#  Delete Questions - working
#  ----------------------------------------------------------------
    @app.route('/questions/<int:question_id>', methods=['DELETE'])
    def delete_question(question_id):
        question = Question.query.get(question_id)
        if not question:
            return abort(404, f'No question found with id: {question_id}')
        question.delete()
        return jsonify({
            'deleted': question_id
        })
#  Submit Question - working
#  ----------------------------------------------------------------
    @app.route('/questions', methods=['POST'])
    def post_question():
        question = request.json.get('question')
        answer = request.json.get('answer')
        category = request.json.get('category')
        difficulty = request.json.get('difficulty')
        if not (question and answer and category and difficulty):
            return abort(400,
                         'Required question object keys missing from request '
                         'body')
        question_entry = Question(question, answer, category, difficulty)
        question_entry.insert()
        return jsonify({
            'question': question_entry.format()
        })
#  Search Questions - not working
#  ----------------------------------------------------------------
    @app.route("/search", methods=['POST'])
    def search_questions():
        if request.data:
            page = 1
            if request.args.get('page'):
                page = int(request.args.get('page'))
            search_data = json.loads(request.data.decode('utf-8'))
            if 'searchTerm' in search_data:
                questions_query = Question.query.filter(
                    Question.question.like(
                        '%' +
                        search_data['searchTerm'] +
                        '%')).paginate(
                    page,
                    QUESTIONS_PER_PAGE,
                    False)
                questions = list(map(Question.format, questions_query.items))
                if len(questions) > 0:
                    result = {
                        "success": True,
                        "questions": questions,
                        "total_questions": questions_query.total,
                        "current_category": None,
                    }
                    return jsonify(result)
            abort(404)
        abort(422)
#  Filter questions via category - working
#  ----------------------------------------------------------------
    @app.route('/categories/<int:category_id>/questions', methods=['GET'])
    def get_questions_by_category(category_id):
        if not category_id:
            return abort(400)
        questions = [question.format() for question in
                     Question.query.filter(Question.category == category_id)]
        return jsonify({
            'questions': questions,
            'total_questions': len(questions),
            'current_category': category_id
        })
#  Play game - render questions with optional category - working
#  ----------------------------------------------------------------
    @app.route("/quizzes", methods=['POST'])
    def get_question_for_quiz():
        body = request.get_json()
        previous_questions = body.get('previous_questions', [])
        quiz_category = body.get('quiz_category', None)

        try:
            if quiz_category:
                if quiz_category['id'] == 0:
                    selections = Question.query.all()
                else:
                    selections = Question.query.filter_by(category=quiz_category['id']).all()

            options =  [question.format() for question in selections if question.id not in previous_questions]
            if len(options) == 0:
                return jsonify({
                    'question': False
                })
            result = random.choice(options)
            return jsonify({
                'question': result
            })
        except:
            abort(500)

# Error Handlers
#  ----------------------------------------------------------------
    @app.errorhandler(422)
    def unprocessable(error):
      return jsonify({
          "success": False,
          "error": 422,
          "message": "Unprocessable"
      }), 422

    @app.errorhandler(404)
    def not_found(error):
      return jsonify({
          "success": False,
          "error": 404,
          "message": "Resource not found"
      }), 404

    @app.errorhandler(400)
    def bad_request(error):
      return jsonify({
          "success": False,
          "error": 400,
          "message": "Bad Request"
      }), 400

    @app.errorhandler(500)
    def server_error(error):
      return jsonify({
          "success": False,
          "error": 500,
          "message": "Server error"
      }), 500

    return app
