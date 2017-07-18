import logging
import traceback

import json
import importlib

import os
import sys

try:
    here = os.path.dirname(os.path.realpath(__file__))
    sys.path.append(os.path.join(here, "./lib"))
    sys.path.append(os.path.join(here, "../lib"))

    import cAuth
    import dynamo

    # https://docs.google.com/document/d/1WFQtcPc03D2fXwOAxg9ihwx-MqgTn0PYMleU-eI5g6k/edit?usp=sharing
except Exception as e:
    traceback.print_exc()

def process(event, context):
    """
    # Use this code if you don't use the http event
    # with the LAMBDA-PROXY integration
    return {
        "message": "Go Serverless v1.0! function execute success!",
        "event": event
    }
    """

    body = {
        "message": "Go Serverless v1.0! Function execute success!",
        "input": event
        # "input": event
    }

    params = event["queryStringParameters"]
    telegram_id = params["state"]
    code = params["code"]

    jsonFlows = dynamo.readFlow(telegram_id)
    #assert(len(jsonFlows) > 0)
    print(jsonFlows)

    jsonFlow = json.loads(jsonFlows[0]["flow"])
    print(jsonFlow)

    flow = cAuth.JsonToFlow(jsonFlow)
    credential = cAuth.authHandleCode(flow, code)
    dynamo.delFlow(telegram_id)
    dynamo.addCredential(telegram_id, credential.to_json())

    return {
        "statusCode": 200,
        "message": "You have been authenticated!"
    }

def respond(event, context):
    try:
        return process(event, context)
    except Exception as e:
        traceback.print_exc()
