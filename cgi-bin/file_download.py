#!/usr/bin/env python3

import cgi
import cgitb
import os
import tempfile

# Enable CGI traceback for debugging
cgitb.enable()

# Print necessary headers
print("Content-Type: application/octet-stream")

# Parse the form data
form = cgi.FieldStorage()
filename = form.getvalue("filename")

# Define the upload directory
upload_dir = os.path.join(tempfile.gettempdir(), "uploads")
file_path = os.path.join(upload_dir, filename)

# Ensure the file exists
if os.path.exists(file_path):
    # Print headers to initiate download
    print(f"Content-Disposition: attachment; filename=\"{filename}\"\n")
    with open(file_path, 'rb') as f:
        print(f.read())
else:
    print("File not found.")
