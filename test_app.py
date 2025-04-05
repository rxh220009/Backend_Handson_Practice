import unittest
import json
from app import app

class TestApp(unittest.TestCase):

    def setUp(self):
        self.app = app.test_client()
        self.app.testing = True

    def test_create_user_empty_name(self):
        response = self.app.post('/users', json={'name': '', 'age': 30})
        self.assertEqual(response.status_code, 400)
        self.assertEqual(json.loads(response.data)['message'], 'Invalid input')

    def test_create_user_age_999(self):
        response = self.app.post('/users', json={'name': 'Test User', 'age': 999})
        self.assertEqual(response.status_code, 201)
        self.assertEqual(json.loads(response.data)['message'], 'User created successfully')

if __name__ == '__main__':
    unittest.main()