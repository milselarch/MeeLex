import traceback
import json

def process(event, context):
    body = {
        "message": "Go Serverless v1.0! Your function executed successfully!",
        "input": event["path"]
        # "input": event
    }

    response = {
        "statusCode": 200,
        "body": json.dumps(body)
    }

    # Use this code if you don't use the http event with the LAMBDA-PROXY integration
    """
    return {
        "message": "Go Serverless v1.0! Your function executed successfully!",
        "event": event
    }
    """

    return response

def respond(event, context):
    try:
        return process(event, context)

    except Exception as e:
        return {
            "statusCode": 403,
            "body": traceback.format_exc()
        }

