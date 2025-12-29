import unittest
from app import app

class AppTestCase(unittest.TestCase):
    def setUp(self):
        self.ctx = app.app_context()
        self.ctx.push()
        self.client = app.test_client()

    def tearDown(self):
        self.ctx.pop()

    def test_home(self):
        response = self.client.get('/')
        self.assertEqual(response.status_code, 200)
        self.assertIn(b'YouTube Downloader', response.data)

    def test_download_no_url(self):
        response = self.client.post('/download', data={}, follow_redirects=True)
        self.assertEqual(response.status_code, 200)
        self.assertIn(b'Please provide a URL', response.data)

if __name__ == '__main__':
    unittest.main()
