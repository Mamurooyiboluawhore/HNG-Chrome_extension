# Video Upload and Playback Application

This is a basic Flask-based web application that allows users to upload video files, store them on the server, and play them back. It uses SQLite for database storage and supports video file format validation.

## Features

- Video upload with validation for allowed file formats (e.g., mp4, mpeg, quicktime).
- Video playback for uploaded videos.
- Listing all uploaded videos with their metadata.

## Prerequisites

Before running the application, make sure you have the following prerequisites installed:

```bash
    pip install flask ```

- Python 3.x
- Flask

## Getting Started

1. Clone this repository to your local machine:

   ```bash
   git clone https://github.com/Mamurooyiboluawhore/HNG-Chrome_extension```
   ```run 
   cd your-repo```

   run the file 
   ```bash
    python app.py ```

# Usage
- Uploading Videos: Access the '/upload' route via a web browser or API to upload videos. Only allowed video formats will be accepted.

- Playing Videos: Access the '/video/<filename>' route to play an uploaded video by specifying its filename.

