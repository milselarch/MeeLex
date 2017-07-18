import json

import boto3
#setup melvin session
msession = boto3.session.Session(
    region_name = 'us-east-1',
    aws_access_key_id = "AKIAIGL5GFHFL6YLHNBA",
    aws_secret_access_key = "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",
)

lexlient = msession.client('lex-runtime')

response = lexlient.post_text(
    botName='BookerApp',
    botAlias='bookapp',
    userId='1111111111111111111',
    sessionAttributes={"String" : "String"},
    inputText='book a room'
)

print(json.dumps(response, indent=4, sort_keys=True))

response = lexlient.post_text(
    botName='BookerApp',
    botAlias='bookapp',
    userId='1111111111111111111',
    sessionAttributes={"String" : "String"},
    inputText='2pm'
)

print(json.dumps(response, indent=4, sort_keys=True))

response = lexlient.post_text(
    botName='BookerApp',
    botAlias='bookapp',
    userId='1111111111111111111',
    sessionAttributes={
        "String" : "String",
    },
    inputText='tomorrow',
)

print(json.dumps(response, indent=4, sort_keys=True))