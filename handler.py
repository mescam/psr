import json
import os
import boto3
import uuid
import pprint
import base64

s3client = boto3.client("s3")
dynamodb = boto3.resource("dynamodb")

bucket = os.getenv("Bucket")
table = dynamodb.Table(os.getenv("Table"))

def get_public_url(bucket, key):
    return "https://s3.us-east-1.amazonaws.com/{}/{}".format(bucket, key)

def list(event, context):
    items = table.scan()["Items"]
    return {
        "body": json.dumps(items),
        "statusCode": 200
    }

def upload(event, context):
    uid = str(uuid.uuid4()) + ".png"
    
    request_body = json.loads(event['body'])

    s3client.put_object(
        Bucket=bucket,
        Key=uid,
        Body=base64.b64decode(request_body["file"]),
        ACL="public-read"
    )

    print("File {} saved as {}".format(request_body["name"], uid))

    table.put_item(Item={
        "ID": uid,
        "FileName": request_body["name"],
        "Result": False,
        "URL": get_public_url(bucket, uid)
    })

    body = {
        "url": get_public_url(bucket, uid)
    }
    response = {
        "statusCode": 200,
        "body": json.dumps(body)
    }

    return response
