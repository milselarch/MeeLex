import boto3
from boto3.dynamodb.conditions import (
    Key, Attr, AttributeExists
)

import time
import config
conf = config.config()

session = boto3.session.Session(
    region_name = conf["awsDynamodbRegion"]
)

dynamodb = session.resource('dynamodb')
table = dynamodb.Table('cxausers')
table.load()

print(table.creation_date_time)

def readCredentials(telegram_id):
    response = table.scan(
        FilterExpression = Attr('telegram_id').eq(
            str(telegram_id)
        ) & Attr("credential").exists()
    )

    return response['Items']

def addCredential(telegram_id, credentialJSON):
    table.put_item(
       Item = {
           'telegram_id': str(telegram_id),
           'credential': credentialJSON,
           'timestamp': str(time.time()),
           'type': "credential"
        }
    )


def readFlow(telegram_id):
    response = table.scan(
        FilterExpression = Attr('telegram_id').eq(
            str(telegram_id)
        ) & Attr("flow").exists()
    )

    return response['Items']

def addFlow(telegram_id, flowJSON):
    table.put_item(
        Item = {
            'telegram_id': str(telegram_id),
            'flow': flowJSON,
            'timestamp': str(time.time()),
            'type': "flow"
        }
    )

def changeToken(telegram_id, credential):
    table.update_item(
        Key = {
            'telegram_id': str(telegram_id)
        },

        UpdateExpression="SET credential = :credential",

        ExpressionAttributeValues = {
            ':credential': credential.to_json(),
        },

        ReturnValues="UPDATED_NEW"
    )

def wipe(telegram_id):
    table.delete_item(
        Key = {
            'telegram_id': telegram_id
        }
    )

if __name__ == "__main__":
    print(table.scan()['Items'])




