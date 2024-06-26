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

    bucket_name = form.getvalue('bucket_name')
    region = form.getvalue('region')
    aws_access_key_id = form.getvalue('aws_access_key_id')
    aws_secret_access_key = form.getvalue('aws_secret_access_key')

    if not all([bucket_name, region, aws_access_key_id, aws_secret_access_key]):
        response = {"error": "All fields are required"}
        print(json.dumps(response))
        return

    try:
        s3_client = boto3.client(
            's3',
            region_name=region,
            aws_access_key_id=aws_access_key_id,
            aws_secret_access_key=aws_secret_access_key
        )

        s3_client.create_bucket(
            Bucket=bucket_name,
            CreateBucketConfiguration={'LocationConstraint': region}
        )

        response = {"message": f"Bucket '{bucket_name}' created successfully in region '{region}'"}
        print(json.dumps(response))

    except (NoCredentialsError, PartialCredentialsError):
        response = {"error": "Invalid AWS credentials"}
        print(json.dumps(response))

    except ClientError as e:
        response = {"error": str(e)}
        print(json.dumps(response))

if __name__ == "__main__":
    main()
