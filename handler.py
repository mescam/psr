import json
import os
import boto3
import uuid

def hello(event, context):
    uid = str(uuid.uuid4())
    s3client = boto3.client("s3")
    s3client.put_object(
        Bucket=os.getenv("Bucket"),
        Key=uid,
        Body=b"1234"
    )

    body = {
        "message": "Go Serverless v1.0! Your function executed successfully!",
        "uid": uid
    }

    response = {
        "statusCode": 200,
        "body": json.dumps(body)
    }

    return response
