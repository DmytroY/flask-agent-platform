import unittest
from app import app

class AppTestCase(unittest.TestCase):
    def setUp(self):
        self.client = app.test_client()
        self.client.testing = True

    def test_get_hello_endpoint(self):
        response = self.client.get('/hello')
        self.assertEqual(response.status_code, 200)
        self.assertIn('What is your name?', response.data.decode('utf-8'))
        self.assertIn('type="text"', response.data.decode('utf-8'))
        self.assertIn('name="name"', response.data.decode('utf-8'))
        self.assertIn('type="submit"', response.data.decode('utf-8'))

    def test_post_hello_endpoint(self):
        response = self.client.post('/hello', data={'name': 'John'}, follow_redirects=True)
        self.assertEqual(response.status_code, 200)
        self.assertIn('Hello', response.data.decode('utf-8'))
        self.assertIn('John', response.data.decode('utf-8'))

if __name__ == '__main__':
    unittest.main()