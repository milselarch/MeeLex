import boto3
from boto3.dynamodb.conditions import Key, Attr

import time

dynamodb = boto3.resource('dynamodb')
table = dynamodb.Table('cxausers')
table.load()

print(table.creation_date_time)

def read(telegram_id):
    response = table.scan(
        FilterExpression=Attr('telegram_id').eq(
            str(telegram_id)
        )
    )

    return response['Items']

def insert(telegram_id, credentialJSON):
    table.put_item(
       Item = {
           'telegram_id': str(telegram_id),
           'credential': credentialJSON,
           'timestamp': str(time.time())
        }
    )

def changeToken(telegram_id, credential):
    table.update_item(
        Key = {
            'telegram_id': str(telegram_id)
        },

        UpdateExpression="SET credential = :credential",

        ExpressionAttributeValues={
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




