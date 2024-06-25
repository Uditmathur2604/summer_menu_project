#!/usr/bin/env python3

import cgi
import cgitb
import os
import tempfile

# Enable CGI traceback for debugging
cgitb.enable()

# Print necessary headers
print("Content-Type: text/html\n")

# Parse the form data
form = cgi.FieldStorage()
upload_file = form['file'] if 'file' in form else None
list_files = form.getvalue("list_files")

# Define the upload directory
upload_dir = os.path.join(tempfile.gettempdir(), "uploads")

# Ensure the upload directory exists
if not os.path.exists(upload_dir):
    os.makedirs(upload_dir)

# Check if there is a file to upload
if upload_file is not None and upload_file.filename:
    # Save the uploaded file
    file_path = os.path.join(upload_dir, upload_file.filename)
    with open(file_path, 'wb') as f:
        f.write(upload_file.file.read())
    print(f"File {upload_file.filename} uploaded successfully!")
# Check if we need to list the files
elif list_files:
    # List the files
    files = os.listdir(upload_dir)
    if files:
        print("<h2>List of Files</h2>")
        print("<table border='1'>")
        print("<tr><th>File Name</th><th>File Size (bytes)</th><th>Actions</th></tr>")
        for file in files:
            file_path = os.path.join(upload_dir, file)
            file_size = os.path.getsize(file_path)
            download_link = f"/cgi-bin/file_download.py?filename={file}"
            print(f"<tr><td>{file}</td><td>{file_size}</td><td><a href='{download_link}'>Download</a></td></tr>")
        print("</table>")
    else:
        print("No files found.")
else:
    print("Invalid request.")
