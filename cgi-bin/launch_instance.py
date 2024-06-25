#!/usr/bin/env python3

import cgi
import cgitb
import json
import boto3

# Enable CGI traceback for debugging
cgitb.enable()

# Print necessary headers
print("Content-Type: application/json\n")

# Parse the form data
form = cgi.FieldStorage()
instance_type = form.getvalue("instanceType")
image_id = form.getvalue("imageId")
aws_access_key = form.getvalue("aws_access_key")
aws_secret_key = form.getvalue("aws_secret_key")
region_name = form.getvalue("regionName")

# Initialize the boto3 resource
ec2_resource = boto3.resource(
    "ec2",
    region_name=region_name,
    aws_access_key_id=aws_access_key,
    aws_secret_access_key=aws_secret_key
)

# Function to launch an EC2 instance
def launch_instance(instance_type, image_id):
    try:
        instance = ec2_resource.create_instances(
            InstanceType=instance_type,
            ImageId=image_id,
            MaxCount=1,
            MinCount=1
        )
        return {"message": "Instance launched successfully", "instance_id": instance[0].id}
    except Exception as e:
        return {"error": str(e)}

# Launch the instance
result = launch_instance(instance_type, image_id)

# Output the result as JSON
print(json.dumps(result))
