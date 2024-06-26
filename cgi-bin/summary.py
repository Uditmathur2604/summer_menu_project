#!/usr/bin/env python3

import cgi
import cgitb
import requests
import re
from youtube_transcript_api import YouTubeTranscriptApi

cgitb.enable()

print("Content-Type: text/html\n")

form = cgi.FieldStorage()
url = form.getvalue("url")

if not url:
    print("<html><body><h2>Error: No URL provided</h2></body></html>")
    exit()

# Improved regex pattern to match various YouTube URL formats
video_id_pattern = (
    r'(?:v=|\/v\/|\/embed\/|youtu\.be\/|\/watch\?v=|&v=|\/shorts\/)'
    r'([a-zA-Z0-9_-]{11})'
)
video_id_match = re.search(video_id_pattern, url)

if not video_id_match:
    print("<html><body><h2>Error: Invalid URL</h2></body></html>")
    exit()

video_id = video_id_match.group(1)

try:
    transcript = YouTubeTranscriptApi.get_transcript(video_id)
    summary = " ".join([item['text'] for item in transcript])
    print(f"<html><body><h2>Video Summary</h2><p>{summary}</p></body></html>")
except Exception as e:
    print(f"<html><body><h2>Error: {str(e)}</h2></body></html>")
