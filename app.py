from flask import Flask, request, send_from_directory, jsonify
import os
import cv2
import numpy as np
import pika
import subprocess
import threading
import time
import uuid
from werkzeug.utils import secure_filename
import speech_recognition as sr
from moviepy.editor import VideoFileClip

app = Flask(__name__)
UPLOAD_FOLDER = 'uploads'
app.config['UPLOAD_FOLDER'] = UPLOAD_FOLDER
ALLOWED_EXTENSIONS = {'mp4', 'mpeg', 'quicktime'}
VIDEO_CHUNK_SIZE = 1024

rabbitmq_host = 'localhost'
rabbitmq_queue = 'video_chunks'

# Video recording variables
video_writer = None
video_filename = None
video_recording = False

# Speech transcription variables
transcription_thread = None
transcribed_text = ""

# Define the missing functions

def allowed_file(filename):
    return '.' in filename and filename.rsplit('.', 1)[1].lower() in ALLOWED_EXTENSIONS

def start_video_recording():
    global video_writer, video_filename, video_recording
    video_filename = os.path.join(app.config['UPLOAD_FOLDER'], f'recorded_video_{str(uuid.uuid4())}.avi')
    fourcc = cv2.VideoWriter_fourcc(*'XVID')
    fps = 20.0
    frame_size = (640, 480)
    video_writer = cv2.VideoWriter(video_filename, fourcc, fps, frame_size)
    video_recording = True

def stop_video_recording():
    global video_writer, video_recording
    if video_writer:
        video_writer.release()
        video_recording = False
        send_video_to_queue(video_filename)

def send_video_to_queue(video_path):
    connection = pika.BlockingConnection(pika.ConnectionParameters(host=rabbitmq_host))
    channel = connection.channel()
    channel.queue_declare(queue=rabbitmq_queue)
    with open(video_path, 'rb') as video_file:
        while True:
            chunk = video_file.read(VIDEO_CHUNK_SIZE)
            if not chunk:
                break
            channel.basic_publish(exchange='', routing_key=rabbitmq_queue, body=chunk)
    connection.close()

def transcribe_video_to_speech(video_path):  # Define the missing function
    try:
        # Load the video and extract audio
        video_clip = VideoFileClip(video_path)
        audio_clip = video_clip.audio

        # Export the audio as a WAV file
        audio_temp_path = os.path.join(app.config['UPLOAD_FOLDER'], 'temp_audio.wav')
        audio_clip.write_audiofile(audio_temp_path, codec='pcm_s16le')

        # Initialize the speech recognition recognizer
        recognizer = sr.Recognizer()

        # Transcribe the audio to text from the temporary WAV file
        with sr.AudioFile(audio_temp_path) as source:
            audio = recognizer.record(source)
            transcribed_text = recognizer.recognize_google(audio)

        # Clean up the temporary audio file
        os.remove(audio_temp_path)

        return transcribed_text
    except Exception as e:
        return f"Transcription error: {str(e)}"

def transcribe_video():
    global transcribed_text
    recognizer = sr.Recognizer()
    audio_temp_path = os.path.join(app.config['UPLOAD_FOLDER'], 'temp_audio.wav')
    audio_clip = VideoFileClip(video_filename).audio
    audio_clip.write_audiofile(audio_temp_path, codec='pcm_s16le')
    with sr.AudioFile(audio_temp_path) as source:
        audio_data = recognizer.record(source)
    try:
        transcribed_text = recognizer.recognize_google(audio_data)
    except sr.UnknownValueError:
        transcribed_text = "Speech recognition could not understand the audio"
    except sr.RequestError as e:
        transcribed_text = f"Could not request results from the speech recognition service; {e}"
    time.sleep(1)

# Rest of your code remains unchanged...

if __name__ == '__main__':
    if not os.path.exists(app.config['UPLOAD_FOLDER']):
        os.makedirs(app.config['UPLOAD_FOLDER'])
    app.run(host='0.0.0.0', debug=True, threaded=True)
