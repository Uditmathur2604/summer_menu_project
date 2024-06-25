#!/usr/bin/env python3

import cgi
import cgitb
import json
from twilio.rest import Client

# Enable CGI traceback for debugging
cgitb.enable()

def send_sms(account_sid, auth_token, twilio_number, recipient_number, message_body):
    client = Client(account_sid, auth_token)
    try:
        message = client.messages.create(
            body=message_body,
            from_=twilio_number,
            to=recipient_number
        )
        return {"message": f"Message sent with SID: {message.sid}"}
    except Exception as e:
        return {"error": str(e)}

# Print necessary headers
print("Content-Type: application/json\n")

# Parse the form data
form = cgi.FieldStorage()
account_sid = form.getvalue("accountSid")
auth_token = form.getvalue("authToken")
twilio_number = form.getvalue("twilioNumber")
recipient_number = form.getvalue("recipientNumber")
message_body = form.getvalue("messageBody")

# Validate input
if not account_sid or not auth_token or not twilio_number or not recipient_number or not message_body:
    response = {"error": "Missing required input"}
else:
    response = send_sms(account_sid, auth_token, twilio_number, recipient_number, message_body)

print(json.dumps(response))
