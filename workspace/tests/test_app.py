import unittest
from app import app

class AppTestCase(unittest.TestCase):
    def setUp(self):
        self.client = app.test_client()
        self.client.testing = True

    def test_health_endpoint(self):
        response = self.client.get('/health')
        self.assertEqual(response.status_code, 200)
        self.assertEqual(response.json, {'status': 'ok'})

    def test_version_endpoint(self):
        response = self.client.get('/version')
        self.assertEqual(response.status_code, 200)
        self.assertEqual(response.json, {'version': '1.0.0'})

if __name__ == '__main__':
    unittest.main()