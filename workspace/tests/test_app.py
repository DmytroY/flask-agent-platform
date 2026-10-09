import unittest
from app import app

class AppTestCase(unittest.TestCase):
    def setUp(self):
        self.client = app.test_client()
        self.client.testing = True

    def test_hello_endpoint(self):
        response = self.client.get('/hello')
        self.assertEqual(response.status_code, 200)
        self.assertIn(b'What is your name?', response.data)

    def test_hello_endpoint_with_name(self):
        response = self.client.post('/hello', data={'name': 'John'}, follow_redirects=True)
        self.assertEqual(response.status_code, 200)
        self.assertIn(b'Hello, John', response.data)

if __name__ == '__main__':
    unittest.main()