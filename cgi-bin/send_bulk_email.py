#!/usr/bin/env python3

import cgi
import cgitb
import smtplib
from email.mime.text import MIMEText
from email.mime.multipart import MIMEMultipart

# Enable CGI traceback for debugging
cgitb.enable()

# Print necessary headers
print("Content-Type: text/plain\n")

# Parse the form data
form = cgi.FieldStorage()
from_email = form.getvalue("fromEmail")
password = form.getvalue("password")
recipient_list = form.getvalue("recipientList").split(',')

# Email content
subject = "Hi, good morning everyone!!!"
body = "This is a test email sent in bulk."

# SMTP server configuration
smtp_server = "smtp.gmail.com"
smtp_port = 587  # Default SMTP port

# Function to send email
def send_email(recipient, subject, body, smtp_server, smtp_port, from_email, password):
    msg = MIMEMultipart()
    msg['From'] = from_email
    msg['To'] = recipient
    msg['Subject'] = subject

    msg.attach(MIMEText(body, 'plain'))

    server = smtplib.SMTP(smtp_server, smtp_port)
    server.starttls()
    server.login(from_email, password)
    server.sendmail(from_email, recipient, msg.as_string())
    server.quit()

# Send bulk emails
for recipient in recipient_list:
    try:
        send_email(recipient.strip(), subject, body, smtp_server, smtp_port, from_email, password)
        print(f"Email sent to {recipient}")
    except Exception as e:
        print(f"Failed to send email to {recipient}. Error: {str(e)}")
