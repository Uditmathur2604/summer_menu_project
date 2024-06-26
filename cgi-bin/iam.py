#!/usr/bin/env python3

import cgi
import cgitb
import json
import boto3
from botocore.exceptions import NoCredentialsError, PartialCredentialsError, ClientError

cgitb.enable()  # Enable debugging

def main():
    print("Content-Type: application/json")
    print()  # End of headers

    form = cgi.FieldStorage()

    username = form.getvalue('username')
    aws_access_key_id = form.getvalue('aws_access_key_id')
    aws_secret_access_key = form.getvalue('aws_secret_access_key')

    if not all([username, aws_access_key_id, aws_secret_access_key]):
        response = {"error": "All fields are required"}
        print(json.dumps(response))
        return

    try:
        iam_client = boto3.client(
            'iam',
            aws_access_key_id=aws_access_key_id,
            aws_secret_access_key=aws_secret_access_key
        )

        iam_client.create_user(UserName=username)

        response = {"message": f"User '{username}' created successfully"}
        print(json.dumps(response))

    except (NoCredentialsError, PartialCredentialsError):
        response = {"error": "Invalid AWS credentials"}
        print(json.dumps(response))

    except ClientError as e:
        response = {"error": str(e)}
        print(json.dumps(response))

if __name__ == "__main__":
    main()
