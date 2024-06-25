#!/usr/bin/env python3

import cgi
import cgitb
import json
import boto3

# Enable CGI traceback for debugging
cgitb.enable()

def aws_client_login(aws_access_key_id, aws_secret_access_key, region_name):
    ec2_client = boto3.client(
        service_name="ec2",
        region_name=region_name,
        aws_access_key_id=aws_access_key_id,
        aws_secret_access_key=aws_secret_access_key
    )
    return ec2_client

def delete_instance(ec2_client, instance_id):
    try:
        response = ec2_client.terminate_instances(InstanceIds=[instance_id])
        return {"message": "Instance Terminated!", "response": response}
    except Exception as e:
        return {"error": str(e)}

# Print necessary headers
print("Content-Type: application/json\n")

# Parse the form data
form = cgi.FieldStorage()
aws_key = form.getvalue("awsKey")
aws_secret = form.getvalue("awsSecret")
region = form.getvalue("region")
instance_id = form.getvalue("instanceId")

# Validate input
if not aws_key or not aws_secret or not region or not instance_id:
    response = {"error": "Missing required input"}
else:
    ec2_client = aws_client_login(aws_key, aws_secret, region)
    response = delete_instance(ec2_client, instance_id)

print(json.dumps(response))
