
#!/usr/bin/env python3

import cgi
import subprocess
import html

print("Content-Type: text/html\n")

form = cgi.FieldStorage()
command = form.getvalue("command")

if command:
    # Escape the command to prevent shell injection
    command = html.escape(command)
    try:
        # Run the `man` command to get the manual of the input command
        result = subprocess.run(['man', command], text=True, capture_output=True)
        output = result.stdout if result.returncode == 0 else result.stderr
    except Exception as e:
        output = str(e)
else:
    output = "No command provided."

# HTML output
print(f"""
<!DOCTYPE html>
<html lang="en">
<head>
    <meta charset="UTF-8">
    <meta name="viewport" content="width=device-width, initial-scale=1.0">
    <title>Linux Command Description</title>
    <style>
        body {{
            font-family: Arial, sans-serif;
            background-color: #1a1a1a; /* Dark background color */
            color: #ffffff; /* White text color */
            padding: 20px;
            line-height: 1.6;
        }}
        h1 {{
            color: #f44336; /* Red color for heading */
        }}
        pre {{
            background-color: #333333;
            padding: 20px;
            overflow: auto;
        }}
        a {{
            color: #ff9800;
        }}
    </style>
</head>
<body>
    <h1>Linux Command Description</h1>
    <form action="/cgi-bin/get_command_description.py" method="post">
        <label for="command">Enter Linux Command:</label>
        <input type="text" id="command" name="command" required>
        <input type="submit" value="Get Description">
    </form>
    <div id="result">
        <pre>{html.escape(output)}</pre>
    </div>
    <a href="/index.html">Back to form</a>
</body>
</html>
""")
