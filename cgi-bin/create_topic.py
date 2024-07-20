#!/usr/bin/env python3

import cgi
import cgitb
import json
import boto3
from botocore.exceptions import BotoCoreError, ClientError
import sys

# Enable CGI traceback for debugging
cgitb.enable()

# Print necessary headers
print("Content-Type: application/json\n")

def create_sns_topic(topic_name, aws_access_key_id, aws_secret_access_key, region_name):
    try:
        sns = boto3.client(
            'sns',
            region_name=region_name,
            aws_access_key_id=aws_access_key_id,
            aws_secret_access_key=aws_secret_access_key
        )

        response = sns.create_topic(Name=topic_name)
        return {"TopicArn": response['TopicArn']}
    except (BotoCoreError, ClientError) as e:
        return {"error": str(e)}

try:
    # Read and parse incoming POST data
    post_data = json.load(sys.stdin)

    topic_name = post_data.get('topicName')
    aws_access_key_id = post_data.get('awsAccessKeyId')
    aws_secret_access_key = post_data.get('awsSecretAccessKey')
    region_name = post_data.get('regionName')

    if topic_name and aws_access_key_id and aws_secret_access_key and region_name:
        result = create_sns_topic(topic_name, aws_access_key_id, aws_secret_access_key, region_name)
        print(json.dumps(result))
    else:
        print(json.dumps({"error": "Missing required parameters."}))
except Exception as e:
    print(json.dumps({"error": "An unexpected error occurred: " + str(e)}))
