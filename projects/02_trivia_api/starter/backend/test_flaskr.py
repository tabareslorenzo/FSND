import os
import unittest
import json
from flask_sqlalchemy import SQLAlchemy

from flaskr import create_app
from models import setup_db, Question, Category


class TriviaTestCase(unittest.TestCase):
    """This class represents the trivia test case"""

    def setUp(self):
        """Define test variables and initialize app."""
        self.app = create_app()
        self.client = self.app.test_client
        self.database_name = "trivia_test"
        self.database_path = "postgres://{}/{}".format('localhost:5432', self.database_name)
        setup_db(self.app, self.database_path)
        self.new_book = {
            'question': 'whats up',
            'answer': 'the sky',
            'difficulty': 1,
            'category': 1
        }

        # binds the app to the current context
        with self.app.app_context():
            self.db = SQLAlchemy()
            self.db.init_app(self.app)
            # create all tables
            self.db.create_all()

    def tearDown(self):
        """Executed after reach test"""
        pass

    """
    TODO
    Write at least one test for each test for successful operation and for expected errors.
    """
    # def test_get_paginated_questions(self):
    #     #call api
    #     res = self.client().get('/questions')
    #     #data returned
    #     data = json.loads(res.data)
    #     self.assertEqual(res.status_code, 200)
    #     self.assertEqual(data['Success'], True)
    #     self.assertTrue(data['totalQuestions'])
    #     self.assertTrue(data['currentCategory'])
    #
    # def test_404_sent_request_beyond_valid_page(self):
    #     res = self.client().get('/questions?page=1000')
    #     data = json.loads(res.data)
    #     self.assertEqual(res.status_code, 404)
    #     self.assertEqual(data['Success'], False)
    #     self.assertEqual(data['message'], 'resource not found')

    # def test_delete_question(self):
    #     res = self.client().delete('/questions/5')
    #     data = json.loads(res.data)
    #
    #     question = Question.query.filter(Question.id == 5).first()
    #     self.assertEqual(question, None)
    #     self.assertEqual(res.status_code, 200)
    #     self.assertEqual(data['Success'], True)
    #     self.assertTrue(data['totalQuestions'])
    #     self.assertTrue(data['questions'])
    #     self.assertEqual(data['deleted'], 5)

    # def test_404_delete_question(self):
    #     res = self.client().delete('/questions/1000')
    #     data = json.loads(res.data)
    #
    #     self.assertEqual(res.status_code, 404)
    #     self.assertEqual(data['Success'], False)
    #     self.assertEqual(data['message'], 'resource not found')
    #
    # def test_get_questions_by_category(self):
    #     res = self.client().get('/categories/2/questions')
    #     data = json.loads(res.data)
    #
    #     self.assertEqual(res.status_code, 200)
    #     self.assertEqual(data['Success'], True)

    # def test_search_questions(self):
    #     res = self.client().post('/questions/search', data = json.dumps({'searchTerm': 'the'} ))
    #     data = json.loads(res.data)
    #
    #     self.assertEqual(res.status_code, 200)
    #     self.assertEqual(data['Success'], True)
    # def test_new_question(self):
    #     res = self.client().post('/questions', data = json.dumps({'question': 'whats up', 'answer': 'the sky', 'difficulty': 1, 'category': 1}))
    #     data = json.loads(res.data)
    #
    #     self.assertEqual(res.status_code, 200)
    #     self.assertEqual(data['Success'], True)
    def test_get_next_question(self):
        previousQuestions = []
        res = self.client().post('/quizzes', data = json.dumps({'previous_questions' : previousQuestions, 'quiz_category': 3}))
        data = json.loads(res.data)

        print(data['question'])
        self.assertEqual(res.status_code, 200)
        self.assertEqual(data['Success'], True)
        self.assertTrue(data['question'])

# Make the tests conveniently executable
if __name__ == "__main__":
    unittest.main()
