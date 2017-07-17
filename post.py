import json
import logging
import os
import uuid
import boto3

dynamodb = boto3.resource('dynamodb')

def post(event, context):
    data = json.loads(event['body'])
    if 'first_name' not in data:
        logging.error("Validation Failed")
        raise Exception("Couldn't create the person record.")

    table = dynamodb.Table(os.environ['DYNAMODB_TABLE'])
    if 'id' not in data:
        data['id'] = str(uuid.uuid1())
    table.put_item(Item=data)
    response = {
        "statusCode": 200,
        "body": json.dumps(data),
        "headers": {
            "Access-Control-Allow-Origin": "*"
        }
    }

    return response
