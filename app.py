from flask import Flask, render_template, request, send_file, jsonify, after_this_request
import yt_dlp
import os
import tempfile
import logging

app = Flask(__name__)
app.secret_key = 'supersecretkey'  # Change this to a random secret key for production

# Configure logging
logging.basicConfig(level=logging.INFO)
logger = app.logger

@app.route('/')
def index():
    return render_template('index.html')

@app.route('/api/info', methods=['POST'])
def get_video_info():
    data = request.get_json()
    url = data.get('url')
    if not url:
        return jsonify({'error': 'Please provide a URL'}), 400

    try:
        ydl_opts = {
            'quiet': True,
            'no_warnings': True,
        }
        with yt_dlp.YoutubeDL(ydl_opts) as ydl:
            logger.info(f"Fetching info for URL: {url}")
            info = ydl.extract_info(url, download=False)

            # Extract relevant info
            video_data = {
                'title': info.get('title'),
                'thumbnail': info.get('thumbnail'),
                'duration': info.get('duration'),
                'uploader': info.get('uploader'),
                'webpage_url': info.get('webpage_url'),
                'formats': [] # Simplified for now, logic handled in download
            }
            return jsonify(video_data)

    except Exception as e:
        logger.error(f"Error fetching video info: {str(e)}")
        return jsonify({'error': str(e)}), 500

@app.route('/download', methods=['POST'])
def download_video():
    url = request.form.get('url')
    format_type = request.form.get('type', 'video') # 'video' or 'audio'

    if not url:
        return "URL is required", 400

    temp_dir = None
    try:
        # Create a temporary directory
        temp_dir = tempfile.mkdtemp()

        # yt-dlp options
        ydl_opts = {
            'outtmpl': os.path.join(temp_dir, '%(title)s.%(ext)s'),
            'noplaylist': True,
            'quiet': True,
        }

        # Configure format based on selection
        if format_type == 'audio':
            ydl_opts['format'] = 'bestaudio/best'
        else:
            # Default to best video+audio (single file if possible, else best)
            ydl_opts['format'] = 'best'

        with yt_dlp.YoutubeDL(ydl_opts) as ydl:
            logger.info(f"Downloading {format_type} from URL: {url}")
            info = ydl.extract_info(url, download=True)
            filename = ydl.prepare_filename(info)

        # Check if file exists (yt-dlp might have slightly different naming if it corrects characters)
        if not os.path.exists(filename):
             # Try to find the file in the temp dir if the exact filename match fails
             files = os.listdir(temp_dir)
             if files:
                 filename = os.path.join(temp_dir, files[0])
             else:
                 raise Exception("File not found after download.")

        logger.info(f"File downloaded to: {filename}")

        @after_this_request
        def remove_file(response):
            try:
                if os.path.exists(filename):
                    os.remove(filename)
                if os.path.exists(temp_dir):
                    os.rmdir(temp_dir)
                logger.info("Temporary files cleaned up.")
            except Exception as e:
                logger.error(f"Error removing temp file: {e}")
            return response

        return send_file(filename, as_attachment=True)

    except Exception as e:
        logger.error(f"Error downloading video: {str(e)}")
        # Clean up temp dir if it was created but request failed before after_this_request
        if temp_dir and os.path.exists(temp_dir):
            try:
                # Remove all files in the directory
                for f in os.listdir(temp_dir):
                    os.remove(os.path.join(temp_dir, f))
                os.rmdir(temp_dir)
                logger.info("Cleaned up temp directory after error.")
            except Exception as cleanup_error:
                logger.error(f"Error cleaning up temp dir: {cleanup_error}")
        return f"Error downloading video: {str(e)}", 500

if __name__ == '__main__':
    app.run(host='0.0.0.0', port=5000)
