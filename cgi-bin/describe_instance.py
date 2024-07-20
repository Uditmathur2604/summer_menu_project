#!/usr/bin/env python3

import cgi
import cgitb
import boto3
import json

# Set your AWS credentials here
aws_access_key_id = '' #ENTER YOUR ACCESS KEY
aws_secret_access_key = '' #ENTER YOUR SECRET KEY
region_name = 'ap-south-1'  # Replace with your AWS region

# Enable debugging
cgitb.enable()

print("Content-Type: application/json")
print()

# Get the instance ID from the form
form = cgi.FieldStorage()
instance_id = form.getvalue('instance_id')

if not instance_id:
    print(json.dumps({"error": "Instance ID is required"}))
    exit()

# Initialize a session using Amazon EC2 with the specified credentials and region
session = boto3.Session(
    aws_access_key_id=aws_access_key_id,
    aws_secret_access_key=aws_secret_access_key,
    region_name=region_name
)

# Create an EC2 client
ec2 = session.client('ec2')

# Describe the instance
try:
    response = ec2.describe_instances(InstanceIds=[instance_id])
    print(json.dumps(response, indent=4, default=str))
except Exception as e:
    print(json.dumps({"error": str(e)}))
