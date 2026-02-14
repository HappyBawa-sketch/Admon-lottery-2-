import unittest
from unittest.mock import patch, MagicMock
from app import app
import json

class AppTestCase(unittest.TestCase):
    def setUp(self):
        self.app = app.test_client()
        self.app.testing = True

    @patch('app.yt_dlp.YoutubeDL')
    def test_get_video_info_success(self, mock_ydl):
        # Mock the context manager and extract_info return value
        mock_instance = mock_ydl.return_value.__enter__.return_value
        mock_instance.extract_info.return_value = {
            'title': 'Test Video',
            'thumbnail': 'http://example.com/thumb.jpg',
            'duration': 120,
            'uploader': 'Test Uploader',
            'webpage_url': 'http://example.com/video',
            'formats': []
        }

        response = self.app.post('/api/info',
                                 data=json.dumps({'url': 'http://example.com/video'}),
                                 content_type='application/json')

        self.assertEqual(response.status_code, 200)
        data = json.loads(response.data)
        self.assertEqual(data['title'], 'Test Video')
        self.assertEqual(data['uploader'], 'Test Uploader')

    @patch('app.yt_dlp.YoutubeDL')
    def test_get_video_info_failure(self, mock_ydl):
        # Mock an exception
        mock_instance = mock_ydl.return_value.__enter__.return_value
        mock_instance.extract_info.side_effect = Exception("Invalid URL")

        response = self.app.post('/api/info',
                                 data=json.dumps({'url': 'http://bad-url'}),
                                 content_type='application/json')

        self.assertEqual(response.status_code, 500)
        data = json.loads(response.data)
        self.assertIn('error', data)

    def test_get_video_info_no_url(self):
        response = self.app.post('/api/info',
                                 data=json.dumps({}),
                                 content_type='application/json')
        self.assertEqual(response.status_code, 400)

    @patch('app.yt_dlp.YoutubeDL')
    @patch('app.os.path.exists')
    @patch('app.os.listdir')
    @patch('app.send_file')
    @patch('app.after_this_request')
    def test_download_video(self, mock_after_request, mock_send_file, mock_listdir, mock_exists, mock_ydl):
        # Setup mocks
        mock_instance = mock_ydl.return_value.__enter__.return_value
        mock_instance.extract_info.return_value = {'title': 'Test', 'ext': 'mp4'}
        mock_instance.prepare_filename.return_value = '/tmp/Test.mp4'

        mock_exists.return_value = True # File exists

        # We need to mock send_file to avoid actual file operations
        mock_send_file.return_value = "File Sent"

        # Mock after_this_request decorator logic (simplified)
        def side_effect(f):
            return f
        mock_after_request.side_effect = side_effect

        response = self.app.post('/download', data={'url': 'http://example.com/video', 'type': 'video'})

        self.assertEqual(response.status_code, 200)
        # Check if correct format was passed to options (best)
        call_args = mock_ydl.call_args[0][0]
        self.assertEqual(call_args['format'], 'best')

    @patch('app.yt_dlp.YoutubeDL')
    @patch('app.os.path.exists')
    @patch('app.os.listdir')
    @patch('app.send_file')
    @patch('app.after_this_request')
    def test_download_audio(self, mock_after_request, mock_send_file, mock_listdir, mock_exists, mock_ydl):
        # Setup mocks
        mock_instance = mock_ydl.return_value.__enter__.return_value
        mock_instance.extract_info.return_value = {'title': 'Test', 'ext': 'm4a'}
        mock_instance.prepare_filename.return_value = '/tmp/Test.m4a'
        mock_exists.return_value = True
        mock_send_file.return_value = "File Sent"
        mock_after_request.side_effect = lambda f: f

        response = self.app.post('/download', data={'url': 'http://example.com/video', 'type': 'audio'})

        self.assertEqual(response.status_code, 200)
        # Check if correct format was passed (bestaudio/best)
        call_args = mock_ydl.call_args[0][0]
        self.assertEqual(call_args['format'], 'bestaudio/best')

if __name__ == '__main__':
    unittest.main()
