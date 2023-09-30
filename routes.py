from flask import Flask, request, send_file
import os
from werkzeug.utils import secure_filename

app = Flask(__name__)
UPLOAD_FOLDER = 'uploads'  # Define the folder for storing uploaded videos
app.config['UPLOAD_FOLDER'] = UPLOAD_FOLDER

def allowed_file(filename):
    allowed_extensions = {'mp4', 'mpeg', 'quicktime'}
    return '.' in filename and filename.rsplit('.', 1)[1].lower() in allowed_extensions

# Video upload route
@app.route('/upload', methods=['POST'])
def upload_video():
    try:
        if 'video' not in request.files:
            return "No file part", 400

        video = request.files['video']

        if video.filename == '':
            return "No selected file", 400

        if not allowed_file(video.filename):
            return "Invalid file format. Supported formats: mp4, mpeg, quicktime", 400

        filename = secure_filename(video.filename)
        # Save the uploaded video without checking if the folder exists
        video.save(os.path.join(app.config['UPLOAD_FOLDER'], filename))
        return "Video uploaded successfully", 200
    except Exception as e:
        # Log the error for debugging purposes
        app.logger.error(f'Video upload failed: {str(e)}')
        return "Internal Server Error", 500

# Video playback route
@app.route('/video/<filename>', methods=['GET'])
def get_video(filename):
    video_path = os.path.join(app.config['UPLOAD_FOLDER'], filename)
    try:
        if os.path.exists(video_path):
            return send_file(video_path)
        else:
            return "Video not found", 404
    except Exception as e:
        app.logger.error(f'Video upload failed: {str(e)}')
        return "Internal Server Error", 500

if __name__ == '__main__':
    app.run(debug=True, port=3000)
