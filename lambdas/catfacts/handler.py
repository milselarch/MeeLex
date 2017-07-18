import traceback
import json

import importlib
dynamo = importlib.__import__('dynamo')
cAuth = importlib.__import__('cAuth')

# https://docs.google.com/document/d/1WFQtcPc03D2fXwOAxg9ihwx-MqgTn0PYMleU-eI5g6k/edit?usp=sharing

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

    flow = cAuth.flowFromJson(dynamo.readFlow(telegram_id))
    credential = cAuth.authHandleCode(flow, code)
    cjson = credential.to_json()

    return {
        "statusCode": 200,
        "body": json.dumps(cjson)
    }


def respond(event, context):
    try:
        return process(event, context)

    except Exception as e:
        return {
            "statusCode": 403,
            "body": traceback.format_exc()
        }


if __name__ == "__main__":
    code = "4/4oLth90iPPUuqtNsFWbCbt-gBugPtk9I0SSyNzJZ8vo"
    print(cAuth.authHandleRequest(code))