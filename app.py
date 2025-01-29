from flask import Flask, request, jsonify
from pytube import YouTube
import os

app = Flask(__name__)

# Folder to store downloaded videos
DOWNLOAD_FOLDER = "downloads"
if not os.path.exists(DOWNLOAD_FOLDER):
    os.makedirs(DOWNLOAD_FOLDER)

@app.route('/')
def home():
    return "YouTube Downloader API is running."

@app.route('/download', methods=['POST'])
def download_video():
    data = request.json
    video_url = data.get('url')

    if not video_url:
        return jsonify({"error": "No URL provided"}), 400

    try:
        yt = YouTube(video_url)
        stream = yt.streams.get_highest_resolution()
        file_path = os.path.join(DOWNLOAD_FOLDER, f"{yt.title}.mp4")
        stream.download(DOWNLOAD_FOLDER)
        return jsonify({"message": "Download complete!", "file": f"https://your-backend-server.com/{file_path}"})
    except Exception as e:
        return jsonify({"error": str(e)}), 500

if __name__ == '__main__':
    app.run(host='0.0.0.0', port=5000)
