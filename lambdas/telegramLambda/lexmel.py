import json

import boto3
import config
conf = config.config()

users = {}

class state(object):
    def __init__(self,ID):
        self.msession = boto3.session.Session(
            aws_access_key_id=conf["AccessID"],
            aws_secret_access_key=conf["AccessSecret"],
            region_name='us-east-1'
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
