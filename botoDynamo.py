import boto3

dynamodb = boto3.resource('dynamodb')
table = dynamodb.Table('cxausers')
table.load()

print(table.creation_date_time)

def insert(telegram_id, token, expiration):
    table.put_item(
       Item = {
           'telegram_id': telegram_id,
           'token': token,
           'expiration': expiration
        }
    )




