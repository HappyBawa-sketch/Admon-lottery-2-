from flask import Flask, render_template, request, send_file, flash, redirect, url_for, after_this_request
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

@app.route('/download', methods=['POST'])
def download_video():
    url = request.form.get('url')
    if not url:
        flash('Please provide a URL')
        return redirect(url_for('index'))

    try:
        # Create a temporary directory
        temp_dir = tempfile.mkdtemp()

        # yt-dlp options
        # Since ffmpeg is not available, we should stick to formats that don't require merging if possible,
        # or accept that some best formats might be video only or audio only.
        # 'best' usually tries to find the best single file if ffmpeg is missing.
        ydl_opts = {
            'format': 'best',
            'outtmpl': os.path.join(temp_dir, '%(title)s.%(ext)s'),
            'noplaylist': True,
            'quiet': True,
        }

        with yt_dlp.YoutubeDL(ydl_opts) as ydl:
            logger.info(f"Downloading from URL: {url}")
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
        flash(f'Error downloading video: {str(e)}')
        return redirect(url_for('index'))

if __name__ == '__main__':
    app.run(host='0.0.0.0', port=5000)
