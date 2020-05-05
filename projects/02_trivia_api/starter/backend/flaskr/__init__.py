import os
import json
from flask import Flask, request, abort, jsonify
from flask_sqlalchemy import SQLAlchemy
from flask_cors import CORS
import random

from models import setup_db, Question, Category

QUESTIONS_PER_PAGE = 10

def create_app(test_config=None):
  # create and configure the app
  app = Flask(__name__)
  setup_db(app)
  app.config['CORS_HEADERS'] = "Content-Type"
  app.config['CORS_RESOURCES'] = {r"/api/*": {"origins": "*"}}


  CORS(app)

  @app.after_request
  def after_request(response):
      response.headers.add('Access-Control-Allow-Headers', 'Content-Type,Authorization,true')
      response.headers.add('Access-Control-Allow-Methods', 'GET, POST, PATCH, DELETE, OPTIONS')
      return response

  @app.route('/quizzes', methods=['POST'])
  def get_next_question():
      data  = json.loads(request.data)
      id = data['quiz_category']['id']
      print(id)
      print(type(id))
      previous_questions = data['previous_questions']

      possible_questions = Question.query.filter(Question.category == int(id)+1).all()

      print(possible_questions)
      print(type(possible_questions))
      question = None

      for possible in possible_questions:
          is_previous = False
          # maybe = possible.id
          for previous in previous_questions:

              print('--')
              print(previous)
              print(possible)
              if previous == possible.id:
                is_previous = True
          if is_previous == False:
              question = possible.format()


      if question is False:
          abort(404)


      return jsonify({
      "Success" : True,
      "question" : question
      })


  def paginate_questions(request, selection):
      page = request.args.get('page', 1, type=int)
      start = (page-1)*QUESTIONS_PER_PAGE
      end = start + QUESTIONS_PER_PAGE

      questions = [question.format() for question in selection]
      current_questions = questions[start:end]

      return current_questions

  def get_categories_tupple(categories_query_results):
      categories = []
      for result in categories_query_results:
          # res = {}
          res = (result.id, result.type)
          categories.append(res)

      return categories


  @app.route('/categories/<category_id>/questions' )
  def get_questions_by_category(category_id):
      selection = Question.query.filter(Question.category == int(category_id)+1).all()
      questions = paginate_questions(request, selection)
      print(questions)

      return jsonify({
        "Success" : True,
        "questions": questions
      })

  @app.route('/questions/search', methods=['POST'])
  def search_question():
      searchTerm = json.loads(request.data)['searchTerm']
      # print(request.data)
      # print('***')
      # print(request.args.get('searchTerm'))
      print(searchTerm)
      search_results = Question.query.filter(Question.question.ilike('%{}%'.format(searchTerm))).all()
      # print(search_results)
      current_questions = paginate_questions(request, search_results)
      if len(current_questions) < 1:
          abort(404)
      print(current_questions[0]['category'])

      return jsonify({
         "Success" : True,
         "questions" : current_questions,
         "currentCategory" : current_questions[0]['category'],
         "totalQuestions" : len(search_results)
       })


  @app.route('/questions', methods=['POST'])
  def create_question():

      print('jwkelrj')
      data = json.loads(request.data)
      print(data)
      print(data['answer'])
      try:
          question = Question(question = data['question'], answer = data['answer'], difficulty = data['difficulty'], category = data['category'])
          question.insert()

          print(question.id)
          # print(Question.query.filter(id = question.id).first)
          selection = Question.query.order_by(Question.id).all()
          current_questions = paginate_questions(request, selection)
          print('--')


      except:

          abort(422)
          print('??')


      return jsonify({
          "Success" : True,
          "created" : question.id,
          "questions" : current_questions,
          "totalQuestions": len(selection)
      })





  @app.route('/questions/<int:question_id>', methods=['DELETE'])
  def delete_question(question_id):
    question = Question.query.filter(Question.id == question_id).first()
    print(question)
    if question == None:
        abort(404)

    question.delete()

    selection = Question.query.order_by(Question.id).all()
    current_questions = paginate_questions(request, selection)
    return jsonify({
        "Success" : True,
        "deleted" : question.id,
        "questions" : current_questions,
        "totalQuestions": len(selection)
    })

  @app.errorhandler(422)
  def unprocessable(error):
      return jsonify({
      "Success" : False,
      "error": 422,
      "message": "unprocessable"
      }), 422
  @app.errorhandler(404)
  def not_found(error):
      return jsonify({
      "Success": False,
      "error" : 404,
      "message" : "resource not found"
      }), 404



  @app.route('/categories')
  def get_categories():
    categories_query_results = Category.query.order_by(Category.id).all()
    categories = get_categories_tupple(categories_query_results)
    print(categories)
    if len(categories) < 1:
        abort(404)
    return jsonify({
    "Success" : True,
    "categories": categories

    })

  @app.route('/questions')
  def get_questions():
      print(request.args)
      selection = Question.query.order_by(Question.id).all()

      questions = paginate_questions(request, selection)
      categories_query_results = Category.query.order_by(Category.id).all()
      categories = get_categories_tupple(categories_query_results)
      print(categories)
      total_questions = len(selection)
      print(total_questions)
      # print(questions[0]['category'])
      print('-----')

      if len(questions) < 1:
          print('ops')
          abort(404)

      return jsonify({
      'Success' : True,
      'questions': questions,
      'totalQuestions': total_questions,
      "categories": categories,
      "currentCategory": questions[0]['category']
      })


  return app
