import json
import logging
import os
import boto3

dynamodb = boto3.resource('dynamodb')

def update(event, context):
    data = json.loads(event['body'])
    if 'first_name' not in data:
        logging.error("Validation Failed")
        raise Exception("Couldn't update the todo item.")

    table = dynamodb.Table(os.environ['DYNAMODB_TABLE'])
    result = table.update_item(
        Key={
            'id': event['pathParameters']['id']
        },
        ExpressionAttributeNames={
            '#first': 'first_name',
            '#last': 'last_name',
            '#birth': 'birthdate',
            '#phone': 'phone_number',
            '#zip': 'zip_code'
        },
        ExpressionAttributeValues={
            ':first': data['first_name'],
            ':last': data['last_name'],
            ':birth': data['birthdate'],
            ':phone': data['phone_number'],
            ':zip': data['zip_code']
        },
        UpdateExpression='SET #first = :first, '
                         '#last = :last, '
                         '#birth = :birth, '
                         '#phone = :phone, '
                         '#zip = :zip',
        ReturnValues='ALL_NEW',
    )

    response = {
        "statusCode": 200,
        "body": json.dumps(result['Attributes']),
        "headers": {
            "Access-Control-Allow-Origin": "*"
        }
    }

    return response
