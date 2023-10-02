# Video Upload and Playback Application

This is a basic Flask-based web application that allows users to upload video files, store them on the server, and play them back. It uses SQLite for database storage and supports video file format validation.

## Features

- Video upload with validation for allowed file formats (e.g., mp4, mpeg, quicktime).
- Video playback for uploaded videos.
- Listing all uploaded videos with their metadata.

## Prerequisites

Before running the application, make sure you have the following prerequisites installed:


    'pip install flask '

- Python 3.x
- Flask

## Getting Started

1. Clone this repository to your local machine:

   ```bash
   git clone https://github.com/Mamurooyiboluawhore/HNG-Chrome_extension```
   'cd your-repo`

   run the file 

    'python app.py '


#API Endpoints
### Start Video Recording
'URL: /start-recording'
- Method: POST
- Description: Starts video recording.
- Response: Returns a message indicating that video recording has started.
### Stop Video Recording
- URL: /stop-recording
- Method: POST
- Description: Stops video recording and initiates the transcription process.
- Response: Returns a message indicating that video recording has stopped.
### Upload Recorded Video
- URL: /upload
- Method: POST
- Description: Uploads a video file for transcription.
- Request Body: Form data with the video file to be uploaded.
- Response: Returns the transcribed text from the uploaded video.
### Get Transcription
- URL: /transcribe
- Method: GET
- Description: Retrieves the transcription of the last recorded video.
- Response: JSON object containing the transcribed text.
### List Available Videos
- URL: /list-videos
- Method: GET
- Description: Lists the available video files in the system.
- Response: JSON object containing a list of available video filenames.
These APIs allow you to record videos, transcribe them, upload videos for transcription, retrieve transcriptions, and list available videos in the system. Make sure to follow the appropriate HTTP methods and request structures when using these endpoints.
