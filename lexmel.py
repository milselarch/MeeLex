import json

import boto3

users = {}

class state(object):
    def __init__(self,ID):
        # setup melvin session
        self.msession = boto3.session.Session(
            region_name='us-east-1',
            aws_access_key_id="AKIAIGL5GFHFL6YLHNBA",
            aws_secret_access_key="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",
        )

        self.lexlient = self.msession.client('lex-runtime')
        self.ID = str(ID)

    def send(self, text):
        response = self.lexlient.post_text(
            botName='BookerApp',
            botAlias='bookapp',
            userId=self.ID,
            sessionAttributes={"String": "String"},
            inputText=text
        )

        return response
