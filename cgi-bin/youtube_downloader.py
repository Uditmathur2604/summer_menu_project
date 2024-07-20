#!/usr/bin/env python3

import cgi
import os
from pytube import YouTube

# Define your downloads directory
DOWNLOADS_DIR = "/var/www/html/downloads/video"

# Function to download video
def download_video(url):
    try:
        yt = YouTube(url)
        stream = yt.streams.get_highest_resolution()
        os.makedirs(DOWNLOADS_DIR, exist_ok=True)
        stream.download(output_path=DOWNLOADS_DIR)
        return f"Video '{yt.title}' downloaded successfully!"
    except Exception as e:
        return f"An error occurred: {str(e)}"

# Function to delete video
def delete_video(file_path):
    try:
        if os.path.exists(file_path):
            os.remove(file_path)
            return f"File '{file_path}' deleted successfully!"
        else:
            return "File not found."
    except Exception as e:
        return f"An error occurred: {str(e)}"

# Main CGI execution
def main():
    print("Content-Type: text/html")
    print()

    form = cgi.FieldStorage()
    action = form.getvalue("action")

    if action == "download":
        url = form.getvalue("url")
        if url:
            message = download_video(url)
        else:
            message = "No URL provided."
    elif action == "delete":
        file_path = form.getvalue("file_path")
        if file_path:
            message = delete_video(file_path)
        else:
            message = "No file path provided."
    else:
        message = ""

    # Print the HTML response
    print(f"""
    <html>
    <head>
        <title>YouTube Downloader</title>
        <style>
            body {{
                background-color: #111;
                color: #fff;
                font-family: Arial, sans-serif;
            }}
            .container {{
                max-width: 600px;
                margin: 50px auto;
                padding: 20px;
                border-radius: 10px;
                background-color: #222;
            }}
            .message {{
                color: #27ae60;
                font-size: 16px;
            }}
            .error {{
                color: #c0392b;
                font-size: 16px;
            }}
            .download-button, .delete-button {{
                background: #d32f2f;
                color: white;
                padding: 10px;
                border: none;
                border-radius: 5px;
                cursor: pointer;
                margin-top: 10px;
            }}
            .file-list {{
                margin-top: 20px;
            }}
            .file-item {{
                background: #333;
                padding: 10px;
                border-radius: 5px;
                margin-bottom: 5px;
                display: flex;
                justify-content: space-between;
            }}
        </style>
    </head>
    <body>
        <div class="container">
            <h1>YouTube Downloader</h1>
            <form action="/cgi-bin/youtube_downloader.py" method="post">
                <input type="hidden" name="action" value="download">
                <label for="url">YouTube URL:</label><br>
                <input type="text" id="url" name="url" required><br><br>
                <input type="submit" value="Download" class="download-button">
            </form>
            <br>
            <div class="message">{message}</div>
            <h2>Downloaded Videos</h2>
            <div class="file-list">
    """)

    # List downloaded videos
    if os.path.exists(DOWNLOADS_DIR):
        for filename in os.listdir(DOWNLOADS_DIR):
            file_path = os.path.join(DOWNLOADS_DIR, filename)
            print(f"""
            <div class="file-item">
                <span>{filename}</span>
                <form action="/cgi-bin/youtube_downloader.py" method="post" style="margin: 0;">
                    <input type="hidden" name="action" value="delete">
                    <input type="hidden" name="file_path" value="{file_path}">
                    <input type="submit" value="Delete" class="delete-button">
                </form>
            </div>
            """)

    print("""
            </div>
        </div>
    </body>
    </html>
    """)

if __name__ == "__main__":
    main()
