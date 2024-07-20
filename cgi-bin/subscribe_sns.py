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

def subscribe_to_sns(topic_arn, protocol, endpoint, aws_access_key_id, aws_secret_access_key, region_name):
    try:
        sns = boto3.client(
            'sns',
            region_name=region_name,
            aws_access_key_id=aws_access_key_id,
            aws_secret_access_key=aws_secret_access_key
        )

        response = sns.subscribe(
            TopicArn=topic_arn,
            Protocol=protocol,
            Endpoint=endpoint
        )
        return {"SubscriptionArn": response['SubscriptionArn']}
    except (BotoCoreError, ClientError) as e:
        return {"error": str(e)}

try:
    # Read and parse incoming POST data
    post_data = json.load(sys.stdin)

    topic_arn = post_data.get('topicArn')
    protocol = post_data.get('protocol')
    endpoint = post_data.get('endpoint')
    aws_access_key_id = post_data.get('awsAccessKeyId')
    aws_secret_access_key = post_data.get('awsSecretAccessKey')
    region_name = post_data.get('regionName')

    if topic_arn and protocol and endpoint and aws_access_key_id and aws_secret_access_key and region_name:
        result = subscribe_to_sns(topic_arn, protocol, endpoint, aws_access_key_id, aws_secret_access_key, region_name)
        print(json.dumps(result))
    else:
        print(json.dumps({"error": "Missing required parameters."}))
except Exception as e:
    print(json.dumps({"error": "An unexpected error occurred: " + str(e)}))
